<script setup>
import InfoBlock from "@/components/ui/InfoBlock.vue";
import InfoGraph from "@/components/ui/InfoGraph.vue";
import WorkersTable from "@/components/tables/WorkersTable.vue";
import Button from "@/components/ui/Button.vue";
import {useWorkers} from "@/composables/useWorkers.js";
import useFarmStatistics from "@/composables/useFarmStatistics.js";
import {computed} from "vue";

const {workers, loading: workersLoading} = useWorkers();
const { statistics, loading: statsLoading, error } = useFarmStatistics();

const isLoading = computed(() => workersLoading || statsLoading);
</script>

<template>
  <div class="home">
    <h1>
      Общая статистика
    </h1>
    <div class="info-blocks">
      <div class="page-block page-info-block">
        <InfoBlock
            title="Курицы"
            href="/chickens"
            subTitle="Общее количество"
            :count="statistics.chickensCount.toString()"
            :loading="statsLoading"
        />
      </div>
      <div class="page-block page-info-block">
        <InfoBlock
            title="Сотрудники"
            href="/employees"
            subTitle="Общее количество"
            :count="statistics.workersCount.toString()"
            :loading="statsLoading"
        />
      </div>
      <div class="page-block page-info-block">
        <InfoBlock
            title="Породы"
            href="/breeds"
            subTitle="Общее количество"
            :count="statistics.breedsCount.toString()"
            :loading="statsLoading"
        />
      </div>
      <div class="page-block page-info-block">
        <InfoBlock
            title="Цехи"
            href="/workshops"
            subTitle="Общее количество"
            :count="statistics.workshopsCount.toString()"
            :loading="statsLoading"
        />
      </div>
      <div class="page-block page-info-block">
        <InfoBlock
            title="Ряды"
            href="/rows"
            subTitle="Общее количество"
            :count="statistics.rowsCount.toString()"
            :loading="statsLoading"
        />
      </div>
      <div class="page-block page-info-block">
        <InfoBlock
            title="Клетки"
            href="/cages"
            subTitle="Общее количество"
            :count="statistics.cagesCount.toString()"
            :loading="statsLoading"
        />
      </div>
    </div>

    <h1>
      Ключевые метрики куриц
    </h1>
    <div class="info-blocks">
      <div class="page-block page-info-block">
        <InfoBlock
            title="Яйценоскость на курицу"
            href="/report-breed-egg-difference"
            subTitle="Средняя"
            :count="statistics.avgEggsPerChicken.toString()"
            :loading="statsLoading"
        />
      </div>
      <div class="page-block page-info-block">
        <InfoBlock
            title="Производство яиц за текущий месяц"
            href="/report-factory-monthly"
            subTitle="Общее количество"
            :count="statistics.totalEggsThisMonth.toString()"
            :loading="statsLoading"
        />
      </div>
      <div class="page-block page-info-block">
        <InfoBlock
            title="Возраст куриц"
            href="/chickens"
            subTitle="Средний"
            :count="`${statistics.avgChickenAge} мес.`"
            :loading="statsLoading"
        />
      </div>
    </div>

<!--    <div class="graph-blocks">-->
<!--      <div class="page-block page-graph-block">-->
<!--        <InfoGraph title="Производство яиц по цехам" image="/images/graph1.png" href="#"/>-->
<!--      </div>-->
<!--      <div class="page-block page-graph-block">-->
<!--        <InfoGraph title="Производство яиц по цехам" image="/images/graph1.png" href="#"/>-->
<!--      </div>-->
<!--      <div class="page-block page-graph-block">-->
<!--        <InfoGraph title="Производство яиц по цехам" image="/images/graph1.png" href="#"/>-->
<!--      </div>-->
<!--    </div>-->
<!--    <div class="table-employees-block page-block">-->
<!--      <div class="table-template__header">-->
<!--        <h2 class="table-template__title">-->
<!--          Лучшие сотрудники-->
<!--        </h2>-->
<!--        <Button-->
<!--            href="/employees"-->
<!--            class="table-template__button"-->
<!--            icon-name="arrow-right"-->
<!--            :icon-width="28"-->
<!--            :icon-height="28"-->
<!--        />-->
<!--      </div>-->
<!--      <Loader v-if="loading===true" />-->
<!--      <WorkersTable-->
<!--          v-if="loading===false"-->
<!--          style="margin-block: 8px"-->
<!--          :headersItem="[-->
<!--              { key: 'name', label: 'Имя' },-->
<!--              { key: 'position', label: 'Должность' }-->
<!--              ]"-->
<!--          :bodyItems="workers"-->
<!--          :height-size="5"-->
<!--      />-->
<!--    </div>-->
  </div>
</template>


<style lang="scss">
.page-block {
  background: var(--section-bg);
  border-radius: 8px;
  padding: 12px 19px 17px 17px;
}

.info-blocks {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-block: 20px;
}

.graph-blocks {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 20px;
}

.page-info-block {
  margin: 0;
  height: 87px;
  background: var(--contrast);

  &:hover {
    transform: scale(1.03);
    transition: 0.15s;
  }
}

.page-graph-block {
  margin: 0;
  background: var(--section-bg);
}

.table-template {
  &__header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  &__title {
    font-size: 16px;
  }
}
</style>