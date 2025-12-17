package http

import (
	"net/http"

	"github.com/go-chi/chi/v5"
	chimiddleware "github.com/go-chi/chi/v5/middleware"
	httpSwagger "github.com/swaggo/http-swagger"
	_ "school-service/docs/swagger"
	"school-service/internal/config"
	"school-service/internal/delivery/http/handler"
	httpmiddleware "school-service/internal/delivery/http/middleware"
	"school-service/internal/domain"
	"school-service/internal/domain/clock"
	"school-service/internal/domain/health"
	"school-service/internal/domain/logger"
	"school-service/internal/domain/usecase"
)

func Router(cfg *config.Config, db health.HealthChecker, clock clock.Clock, log logger.Logger, jwtService domain.JWTService, teacherUC usecase.TeacherUseCase, studentUC usecase.StudentUseCase, classUC usecase.ClassUseCase, scheduleUC usecase.ScheduleUseCase, gradeUC usecase.GradeUseCase, infoUC usecase.InfoUseCase, reportUC usecase.ReportUseCase, authUC usecase.AuthUseCase) http.Handler {
	r := chi.NewRouter()

	r.Use(chimiddleware.RequestID)
	r.Use(chimiddleware.RealIP)
	r.Use(httpmiddleware.LoggerMiddleware(log, clock))
	r.Use(chimiddleware.Recoverer)

	// Настройка CORS из конфига
	r.Use(httpmiddleware.CORS(cfg.CORS))

	// Swagger UI
	r.Get("/swagger/*", httpSwagger.Handler(
		httpSwagger.URL("/swagger/doc.json"),
	))

	healthHandler := handler.NewHealthHandler(db, clock, log)

	r.Route("/health", func(r chi.Router) {
		r.Get("/", healthHandler.Check)
		r.Head("/", healthHandler.Check)
		r.Get("/ready", healthHandler.Ready)
		r.Head("/ready", healthHandler.Ready)
		r.Get("/live", healthHandler.Live)
		r.Head("/live", healthHandler.Live)
	})

	// Публичные маршруты для аутентификации
	authHandler := handler.NewAuthHandler(authUC, log)
	r.Route("/api/v1/auth", func(r chi.Router) {
		r.Post("/register", authHandler.Register)
		r.Post("/login", authHandler.Login)
		r.Post("/refresh", authHandler.RefreshToken)
		r.Post("/logout", authHandler.Logout)
	})

	// Защищенные маршруты (требуют аутентификации)
	r.Group(func(r chi.Router) {
		r.Use(httpmiddleware.AuthMiddleware(jwtService))

		teacherHandler := handler.NewTeacherHandler(teacherUC, log)
		r.Route("/api/v1/teachers", func(r chi.Router) {
			// GET доступны всем аутентифицированным
			r.Get("/", teacherHandler.List)
			r.Get("/{id}", teacherHandler.GetByID)

			// CRUD только для admin
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin)).Post("/", teacherHandler.Create)
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin)).Put("/{id}", teacherHandler.Update)
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin)).Delete("/{id}", teacherHandler.Delete)
		})

		studentHandler := handler.NewStudentHandler(studentUC, log)
		r.Route("/api/v1/students", func(r chi.Router) {
			// GET доступны всем аутентифицированным
			r.Get("/", studentHandler.List)
			r.Get("/{id}", studentHandler.GetByID)
			r.Get("/class/{classId}", studentHandler.ListByClassID)

			// CRUD только для admin
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin)).Post("/", studentHandler.Create)
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin)).Put("/{id}", studentHandler.Update)
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin)).Delete("/{id}", studentHandler.Delete)
		})

		classHandler := handler.NewClassHandler(classUC, log)
		r.Route("/api/v1/classes", func(r chi.Router) {
			// GET доступны всем аутентифицированным
			r.Get("/", classHandler.List)
			r.Get("/{id}", classHandler.GetByID)
			r.Get("/academic-year/{academicYearId}", classHandler.ListByAcademicYearID)

			// CRUD только для admin
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin)).Post("/", classHandler.Create)
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin)).Put("/{id}", classHandler.Update)
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin)).Delete("/{id}", classHandler.Delete)
		})

		scheduleHandler := handler.NewScheduleHandler(scheduleUC, log)
		r.Route("/api/v1/schedules", func(r chi.Router) {
			// GET доступны всем аутентифицированным
			r.Get("/", scheduleHandler.List)
			r.Get("/{id}", scheduleHandler.GetByID)
			r.Get("/class/{classId}", scheduleHandler.ListByClassID)
			r.Get("/class/{classId}/weekday/{weekdayId}/lesson/{lessonNumber}", scheduleHandler.GetByClassAndWeekdayAndLesson)

			// CRUD только для admin
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin)).Post("/", scheduleHandler.Create)
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin)).Put("/{id}", scheduleHandler.Update)
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin)).Delete("/{id}", scheduleHandler.Delete)
		})

		gradeHandler := handler.NewGradeHandler(gradeUC, log)
		r.Route("/api/v1/grades", func(r chi.Router) {
			// GET доступны всем аутентифицированным
			r.Get("/", gradeHandler.List)
			r.Get("/{id}", gradeHandler.GetByID)
			r.Get("/student/{studentId}", gradeHandler.ListByStudentID)
			r.Get("/class/{classId}", gradeHandler.ListByClassID)
			r.Get("/subject/{subjectId}", gradeHandler.ListBySubjectID)
			r.Get("/class/{classId}/subject/{subjectId}", gradeHandler.ListByClassAndSubject)
			r.Get("/class/{classId}/grading-period/{gradingPeriodId}", gradeHandler.ListByClassAndGradingPeriod)

			// CRUD для admin и teacher
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin, domain.RoleTeacher)).Post("/", gradeHandler.Create)
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin, domain.RoleTeacher)).Put("/{id}", gradeHandler.Update)
			r.With(httpmiddleware.RequireRole(domain.RoleAdmin, domain.RoleTeacher)).Delete("/{id}", gradeHandler.Delete)
		})

		// Info и Reports доступны всем аутентифицированным
		infoHandler := handler.NewInfoHandler(infoUC, log)
		r.Route("/api/v1/info", func(r chi.Router) {
			r.Get("/teachers-count-by-subject", infoHandler.GetTeachersCountBySubject)
			r.Get("/teachers-by-same-subjects", infoHandler.GetTeachersBySameSubjects)
			r.Get("/students-count-by-gender", infoHandler.GetStudentsCountByGender)
			r.Get("/classrooms-count-by-type", infoHandler.GetClassroomsCountByType)
		})

		reportHandler := handler.NewReportHandler(reportUC, log)
		r.Route("/api/v1/reports", func(r chi.Router) {
			r.Get("/class-performance", reportHandler.GetClassPerformanceReport)
		})
	})

	return r
}
