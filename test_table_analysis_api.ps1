#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Примеры тестирования API анализа таблиц через PowerShell

.DESCRIPTION
    Этот скрипт содержит примеры запросов к API /api/table-analysis
    для анализа первых N строк таблицы через нейросети.

.EXAMPLE
    .\test_table_analysis_api.ps1
#>

param(
    [string]$BaseUrl = "http://localhost:3000",
    [string]$FilePath = "uploads/test.csv",
    [int]$RowsCount = 15
)

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          API Table Analysis Test Examples                     ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# Пример 1: Анализ с параметрами по умолчанию (15 строк)
# ============================================================================

Write-Host "📌 Пример 1: Анализ с параметрами по умолчанию (15 строк)" -ForegroundColor Yellow
Write-Host "───────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$example1 = @{
    Method  = "POST"
    Uri     = "$BaseUrl/api/table-analysis"
    Headers = @{
        "Content-Type" = "application/json"
    }
    Body    = @{} | ConvertTo-Json
}

Write-Host "Команда curl:" -ForegroundColor Green
Write-Host "curl -X POST $($example1.Uri) -H 'Content-Type: application/json' -d '{}'"
Write-Host ""
Write-Host "Команда PowerShell:" -ForegroundColor Green
Write-Host @"
`$response = Invoke-RestMethod @{
    Method  = "POST"
    Uri     = "$($example1.Uri)"
    Headers = @{ "Content-Type" = "application/json" }
    Body    = "{}"
}
`$response | ConvertTo-Json | Write-Host
"@
Write-Host ""

# ============================================================================
# Пример 2: Анализ с пользовательским количеством строк
# ============================================================================

Write-Host "📌 Пример 2: Анализ первых 10 строк" -ForegroundColor Yellow
Write-Host "───────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$example2Body = @{
    rows_count = 10
} | ConvertTo-Json

Write-Host "Команда curl:" -ForegroundColor Green
Write-Host "curl -X POST $BaseUrl/api/table-analysis \" -NoNewline
Write-Host ""
Write-Host "  -H 'Content-Type: application/json' \" 
Write-Host "  -d '{""rows_count"": 10}'"
Write-Host ""
Write-Host "Команда PowerShell:" -ForegroundColor Green
Write-Host @"
`$body = @{
    rows_count = 10
} | ConvertTo-Json

`$response = Invoke-RestMethod -Method POST `
    -Uri "$BaseUrl/api/table-analysis" `
    -Headers @{ "Content-Type" = "application/json" } `
    -Body `$body

`$response | ConvertTo-Json | Write-Host
"@
Write-Host ""

# ============================================================================
# Пример 3: Анализ 20 строк
# ============================================================================

Write-Host "📌 Пример 3: Анализ первых 20 строк" -ForegroundColor Yellow
Write-Host "───────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

Write-Host "curl -X POST $BaseUrl/api/table-analysis \" -NoNewline
Write-Host ""
Write-Host "  -H 'Content-Type: application/json' \" 
Write-Host "  -d '{""rows_count"": 20}'"
Write-Host ""

# ============================================================================
# Практический пример с PowerShell функцией
# ============================================================================

Write-Host "📌 Практический пример: PowerShell функция" -ForegroundColor Yellow
Write-Host "───────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$psFunction = @'
function Invoke-TableAnalysis {
    param(
        [string]$BaseUrl = "http://localhost:3000",
        [int]$RowsCount = 15
    )
    
    $uri = "$BaseUrl/api/table-analysis"
    $body = @{
        rows_count = $RowsCount
    } | ConvertTo-Json
    
    Write-Host "🔄 Отправляю запрос на анализ ($RowsCount строк)..." -ForegroundColor Cyan
    
    try {
        $response = Invoke-RestMethod -Method POST `
            -Uri $uri `
            -Headers @{ "Content-Type" = "application/json" } `
            -Body $body `
            -ErrorAction Stop
        
        Write-Host "✅ Запрос успешен!" -ForegroundColor Green
        
        # GigaChat результат
        if ($response.giga_result) {
            Write-Host ""
            Write-Host "📊 GigaChat анализ:" -ForegroundColor Cyan
            Write-Host $response.giga_result
        } else {
            Write-Host "⚠️  GigaChat результат недоступен" -ForegroundColor Yellow
            if ($response.errors.giga_chat) {
                Write-Host "   Ошибка: $($response.errors.giga_chat)" -ForegroundColor Red
            }
        }
        
        # Proxy API результат
        if ($response.proxy_result) {
            Write-Host ""
            Write-Host "🤖 Proxy API анализ:" -ForegroundColor Cyan
            Write-Host $response.proxy_result
        } else {
            Write-Host "⚠️  Proxy API результат недоступен" -ForegroundColor Yellow
            if ($response.errors.proxy_api) {
                Write-Host "   Ошибка: $($response.errors.proxy_api)" -ForegroundColor Red
            }
        }
        
        return $response
    }
    catch {
        Write-Host "❌ Ошибка при отправке запроса:" -ForegroundColor Red
        Write-Host $_.Exception.Message
        return $null
    }
}

# Использование
Invoke-TableAnalysis -BaseUrl "http://localhost:3000" -RowsCount 15
'@

Write-Host $psFunction
Write-Host ""

# ============================================================================
# Сценарий полного использования
# ============================================================================

Write-Host "📌 Сценарий: Полный рабочий процесс" -ForegroundColor Yellow
Write-Host "───────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$workflowExample = @'
# Шаг 1: Загружаем файл
$file = Get-Item "uploads/test.csv"
$response = Invoke-RestMethod -Method POST `
    -Uri "http://localhost:3000/api/upload" `
    -Form @{
        file = $file
    }
Write-Host "✅ Файл загружен: $($response.filename)"

# Шаг 2: Анализируем первые 15 строк
$analysisResponse = Invoke-RestMethod -Method POST `
    -Uri "http://localhost:3000/api/table-analysis" `
    -Headers @{ "Content-Type" = "application/json" } `
    -Body @{ rows_count = 15 } | ConvertTo-Json

Write-Host "✅ Анализ завершен"

# Шаг 3: Выводим результаты
if ($analysisResponse.giga_result) {
    Write-Host "GigaChat: $($analysisResponse.giga_result)"
}

if ($analysisResponse.proxy_result) {
    Write-Host "Proxy API: $($analysisResponse.proxy_result)"
}

# Шаг 4: Получаем исходные данные
$dataResponse = Invoke-RestMethod -Method GET `
    -Uri "http://localhost:3000/api/data?offset=0&limit=15"

Write-Host "📊 Первые 15 строк таблицы:"
$dataResponse.rows | Format-Table -AutoSize
'@

Write-Host $workflowExample
Write-Host ""

# ============================================================================
# Проверка состояния API
# ============================================================================

Write-Host "📌 Проверка доступности API" -ForegroundColor Yellow
Write-Host "───────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray

function Test-TableAnalysisAPI {
    param(
        [string]$BaseUrl = "http://localhost:3000"
    )
    
    Write-Host "Проверяю доступность API..." -ForegroundColor Cyan
    
    try {
        # Проверяем основной endpoint
        $response = Invoke-RestMethod -Method GET `
            -Uri "$BaseUrl/" `
            -ErrorAction Stop
        
        Write-Host "✅ API доступен" -ForegroundColor Green
        
        # Пробуем отправить запрос анализа (должна быть ошибка "нет данных")
        $testResponse = Invoke-RestMethod -Method POST `
            -Uri "$BaseUrl/api/table-analysis" `
            -Headers @{ "Content-Type" = "application/json" } `
            -Body "{}" `
            -ErrorAction SilentlyContinue
        
        if ($testResponse.status -eq "error" -and $testResponse.message -like "*No data*") {
            Write-Host "✅ Endpoint /api/table-analysis работает" -ForegroundColor Green
            Write-Host "   (Ошибка 'No data' ожидается, т.к. файл не загружен)" -ForegroundColor Gray
        }
        
        return $true
    }
    catch {
        Write-Host "❌ API недоступен или произошла ошибка:" -ForegroundColor Red
        Write-Host $_.Exception.Message
        return $false
    }
}

if (Test-TableAnalysisAPI -BaseUrl $BaseUrl) {
    Write-Host ""
    Write-Host "ℹ️  Для полного тестирования:" -ForegroundColor Cyan
    Write-Host "1. Загрузите файл: POST /api/upload"
    Write-Host "2. Анализируйте данные: POST /api/table-analysis"
    Write-Host "3. Получите результаты"
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                    End of Examples                            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
