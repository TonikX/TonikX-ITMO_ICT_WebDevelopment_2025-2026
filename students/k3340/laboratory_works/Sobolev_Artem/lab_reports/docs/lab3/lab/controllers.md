# Пример контроллера

## Краткое описание

- Базовый путь: `/api/v1/chickens`
- Функциональность: создание, получение списка, чтение по ID, полная и частичная замена, удаление
- Документация: аннотации `@Tag`, `@Operation`, `@Parameter` - отображение в Swagger UI
- Оптимистическая блокировка: для методов `PUT`, `PATCH`, `DELETE` используется заголовок If-Match с ETag текущей версии ресурса

## Основные эндпоинты

| Метод    | Путь                  | Назначение            |
| -------- | --------------------- | --------------------- |
| `POST`   | /api/v1/chickens      | Создание новой курицы |
| `GET`    | /api/v1/chickens      | Получение списка кур  |
| `GET`    | /api/v1/chickens/{id} | Получение по ID       |
| `PUT`    | /api/v1/chickens/{id} | Полная замена         |
| `PATCH`  | /api/v1/chickens/{id} | Частичное обновление  |
| `DELETE` | /api/v1/chickens/{id} | Удаление              |

## Код

```Java
@Slf4j
@RestController
@RequestMapping(value = "/api/v1/chickens", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
@Tag(name = "Chickens", description = "Chicken operations")
public class ChickenController {

    private final ChickenService chickenService;

    @Operation(summary = "Create a chicken", description = "Creates a new chicken entity.")
    @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<ChickenDTO>> create(@Valid @RequestBody ChickenPostRequest request) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        ChickenDTO response = chickenService.create(request);
        return ResponseEntity.created(LocationUtils.buildLocation(response.id()))
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "List all chickens", description = "Returns all chickens.")
    @GetMapping
    public ResponseEntity<IamResponse<List<ChickenDTO>>> getAll() {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        List<ChickenDTO> response = chickenService.getAll();
        return ResponseEntity.status(HttpStatus.OK).body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Get chicken by ID", description = "Returns a single chicken by its unique identifier.")
    @GetMapping("/{id}")
    public ResponseEntity<IamResponse<ChickenDTO>> get(
            @Parameter(description = "Chicken identifier", example = "42") @PathVariable(name = "id") Long id) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        ChickenDTO response = chickenService.get(id);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Replace a chicken", description = "Fully replaces a chicken by ID.")
    @PutMapping(value = "/{id}", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<ChickenDTO>> replace(
            @Parameter(description = "Chicken identifier", example = "42") @PathVariable(name = "id") Long id,
            @Valid @RequestBody ChickenPutRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false)
            String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        ChickenDTO response = chickenService.replace(id, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Partially update a chicken", description = "Applies a partial update to a chicken by ID.")
    @PatchMapping(value = "/{id}", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<IamResponse<ChickenDTO>> update(
            @Parameter(description = "Chicken identifier", example = "42") @PathVariable(name = "id") Long id,
            @Valid @RequestBody ChickenPatchRequest request,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false)
            String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        ChickenDTO response = chickenService.update(id, request, expected);
        return ResponseEntity.status(HttpStatus.OK)
                             .eTag(EtagUtils.toEtag(response.version()))
                             .body(IamResponse.createSuccessful(response));
    }

    @Operation(summary = "Delete a chicken", description = "Deletes a chicken by its unique identifier.")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @Parameter(description = "Chicken identifier", example = "42") @PathVariable(name = "id") Long id,
            @Parameter(name = "If-Match",
                       in = ParameterIn.HEADER,
                       required = true,
                       description = "ETag of the resource") @RequestHeader(value = "If-Match", required = false)
            String ifMatch) {
        log.trace(ApiLogMessage.NAME_OF_CURRENT_METHOD.getValue(), LogUtils.getMethodName());
        long expected = EtagUtils.parseIfMatch(ifMatch);
        chickenService.delete(id, expected);
        return ResponseEntity.status(HttpStatus.NO_CONTENT).eTag(ifMatch).build();
    }
}
```
