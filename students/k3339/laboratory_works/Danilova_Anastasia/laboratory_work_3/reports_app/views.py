from collections import defaultdict

from django.db.models import Count
from parks_app.models import PlantWorkerAssignment, Object
from parks_app.models import PlantWorkerAssignment, Object
from parks_app.serializers import *
from parks_app.serializers import *
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .serializers import WorkerObjectPlantCountSerializer


# Create your views here.


class ObjectStatusReportView(generics.ListAPIView):
    def get(self, request):
        total = Object.objects.count()
        serviced = Object.objects.filter(contracts__is_active=True).distinct().count()

        return Response({'total': total,
                         'serviced': serviced,
                         'unserviced': total - serviced,
                         'serviced_percent': round(serviced / total * 100, 1) if total > 0 else 0
                         })


class WorkerObjectCountView(generics.ListAPIView):
    serializer_class = WorkerWithObjectsSerializer
    queryset = Worker.objects.all()


class WorkerColleaguesListAPIView(generics.ListAPIView):
    serializer_class = WorkerSerializer

    def get_queryset(self):
        worker_id = self.kwargs['pk']

        return Worker.objects.filter(
            object_assignments__end_date__isnull=True,
            object_assignments__object_id__in=ObjectWorkerAssignment.objects.filter(
                worker_id=worker_id,
                end_date__isnull=True
            ).values('object_id')
        ).exclude(
            id=worker_id
        ).distinct()


class MostPlantedSpeciesPerObjectView(APIView):

    def get(self, request):
        serviced_objects = Object.objects.filter(
            contracts__is_active=True
        ).distinct()

        results = []

        for obj in serviced_objects:
            species_stats = (
                PlantPlacement.objects
                .filter(zone__object_id=obj)
                .values('plant__species__name')
                .annotate(count=Count('id'))
                .order_by('-count')
            )

            if not species_stats.exists():
                continue

            top_species = species_stats.first()

            results.append({
                'object_id': obj.id,
                'object_name': obj.name,
                'most_planted_species': top_species['plant__species__name'],
                'most_planted_species_count': top_species['count']
            })

        serializer = MostPlantedSpeciesPerObjectSerializer(results, many=True)
        return Response(serializer.data)



class WorkerPlantsPerObjectView(APIView):

    def get(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if not date_from or not date_to:
            raise ValidationError(
                "Необходимо передать date_from и date_to (YYYY-MM-DD)"
            )

        queryset = (
            PlantWorkerAssignment.objects
            .filter(
                date__range=[date_from, date_to],
                plant__placements__zone__object_id__contracts__is_active=True
            )
            .values(
                'worker_id',
                'worker__last_name',
                'worker__first_name',
                'worker__middle_name',
                'plant__placements__zone__object_id__id',
                'plant__placements__zone__object_id__name'
            )
            .annotate(
                plants_count=Count('plant', distinct=True)
            )
            .order_by(
                'worker__last_name',
                'plant__placements__zone__object_id__name'
            )
        )

        results = []
        for row in queryset:
            full_name = f"{row['worker__last_name']} {row['worker__first_name'][0]}."
            if row['worker__middle_name']:
                full_name += f"{row['worker__middle_name'][0]}."

            results.append({
                'worker_id': row['worker_id'],
                'worker_name': full_name,
                'object_id': row['plant__placements__zone__object_id__id'],
                'object_name': row['plant__placements__zone__object_id__name'],
                'plants_count': row['plants_count']
            })

        serializer = WorkerObjectPlantCountSerializer(results, many=True)
        return Response(serializer.data)


class PlantsByLifeFormReportView(APIView):

    def get(self, request):
        queryset = (
            PlantPlacement.objects
            .filter(
                zone__object_id__contracts__is_active=True
            )
            .values(
                'zone__object_id__id',
                'zone__object_id__name',
                'plant__species__name',
                'plant__species__life_form__name'
            )
            .annotate(count=Count('plant', distinct=True))
        )

        report = defaultdict(lambda: {
            'object_total': 0,
            'life_forms': defaultdict(lambda: {
                'life_form_total': 0,
                'species': []
            })
        })

        total_plants = 0

        for row in queryset:
            obj_id = row['zone__object_id__id']
            obj_name = row['zone__object_id__name']
            species = row['plant__species__name']
            life_form = row['plant__species__life_form__name']
            count = row['count']

            report[obj_id]['object_name'] = obj_name
            report[obj_id]['object_total'] += count
            report[obj_id]['life_forms'][life_form]['life_form_total'] += count
            report[obj_id]['life_forms'][life_form]['species'].append({
                'species': species,
                'count': count
            })

            total_plants += count

        objects_result = []
        for obj_id, obj_data in report.items():
            life_forms_list = []
            for lf_name, lf_data in obj_data['life_forms'].items():
                life_forms_list.append({
                    'life_form': lf_name,
                    **lf_data
                })

            objects_result.append({
                'object_id': obj_id,
                'object_name': obj_data['object_name'],
                'object_total': obj_data['object_total'],
                'life_forms': life_forms_list
            })

        serializer = PlantsSummaryReportSerializer({
            'total_plants': total_plants,
            'objects': objects_result
        })

        return Response(serializer.data)
