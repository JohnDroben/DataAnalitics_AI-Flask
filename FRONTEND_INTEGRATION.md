# 🎨 Интеграция анализа таблиц в фронтенд

**Полное руководство для добавления функции анализа AI на страницу**

---

## 📋 Содержание

1. [HTML разметка](#html-разметка)
2. [CSS стили](#css-стили)
3. [JavaScript код](#javascript-код)
4. [Полный пример](#полный-пример)
5. [Интеграция в существующую структуру](#интеграция-в-существующую-структуру)

---

## HTML разметка

### Минимальная разметка

```html
<!-- Кнопка для запуска анализа -->
<button id="analyze-btn" onclick="analyzeTable()">
  Анализировать первые 15 строк
</button>

<!-- Контейнер для результатов -->
<div id="analysis-results" style="display: none;">
  <div class="result-block">
    <h3>🤖 GigaChat Анализ</h3>
    <p id="giga-result"></p>
  </div>
  <div class="result-block">
    <h3>🤖 Proxy API Анализ</h3>
    <p id="proxy-result"></p>
  </div>
</div>
```

### Расширенная разметка

```html
<div class="analysis-panel">
  <!-- Заголовок -->
  <h2>📊 AI Анализ таблицы</h2>
  
  <!-- Контрольная панель -->
  <div class="analysis-controls">
    <!-- Выбор количества строк -->
    <div class="control-group">
      <label for="rows-count">Количество строк:</label>
      <input type="number" 
             id="rows-count" 
             value="15" 
             min="1" 
             max="100"
             placeholder="Введите количество строк">
    </div>
    
    <!-- Кнопки управления -->
    <div class="control-buttons">
      <button id="analyze-btn" class="btn btn-primary" onclick="analyzeTable()">
        <span class="btn-icon">🚀</span>
        Анализировать
      </button>
      
      <button id="reset-btn" class="btn btn-secondary" onclick="resetAnalysis()">
        <span class="btn-icon">🔄</span>
        Очистить
      </button>
    </div>
  </div>
  
  <!-- Индикатор загрузки -->
  <div id="loading-indicator" class="loading-indicator" style="display: none;">
    <div class="spinner"></div>
    <p>Анализируем данные...</p>
  </div>
  
  <!-- Результаты анализа -->
  <div id="analysis-results" class="analysis-results" style="display: none;">
    <!-- GigaChat результат -->
    <div class="result-block result-giga">
      <div class="result-header">
        <h3>📊 Анализ GigaChat</h3>
        <button class="btn-copy" onclick="copyToClipboard('giga')">
          📋 Копировать
        </button>
      </div>
      <div class="result-content">
        <p id="giga-result" class="result-text">Ожидание результата...</p>
        <div id="giga-error" class="error-message" style="display: none;"></div>
      </div>
    </div>
    
    <!-- Proxy API результат -->
    <div class="result-block result-proxy">
      <div class="result-header">
        <h3>🤖 Анализ Proxy API</h3>
        <button class="btn-copy" onclick="copyToClipboard('proxy')">
          📋 Копировать
        </button>
      </div>
      <div class="result-content">
        <p id="proxy-result" class="result-text">Ожидание результата...</p>
        <div id="proxy-error" class="error-message" style="display: none;"></div>
      </div>
    </div>
  </div>
  
  <!-- Информационное сообщение -->
  <div id="info-message" class="info-message" style="display: none;"></div>
</div>
```

---

## CSS стили

### Основные стили

```css
/* Основной контейнер */
.analysis-panel {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 12px;
  padding: 24px;
  margin: 20px 0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.analysis-panel h2 {
  margin-top: 0;
  color: #333;
  font-size: 28px;
  margin-bottom: 24px;
}

/* Контрольная панель */
.analysis-controls {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
  align-items: center;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-group label {
  font-weight: 600;
  color: #555;
}

.control-group input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  width: 100px;
}

/* Кнопки управления */
.control-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: #e8eef7;
  color: #333;
  border: 1px solid #d0d8e8;
}

.btn-secondary:hover {
  background: #d8dfe7;
}

.btn-icon {
  font-size: 16px;
}

.btn-copy {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-size: 14px;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.btn-copy:hover {
  background: rgba(102, 126, 234, 0.1);
}

/* Спиннер загрузки */
.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  text-align: center;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-indicator p {
  color: #666;
  font-size: 16px;
}

/* Результаты анализа */
.analysis-results {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 24px;
}

@media (max-width: 768px) {
  .analysis-results {
    grid-template-columns: 1fr;
  }
  
  .analysis-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .control-group {
    flex-direction: column;
  }
  
  .control-group input {
    width: 100%;
  }
}

/* Блок результата */
.result-block {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-left: 4px solid #667eea;
  transition: all 0.3s ease;
}

.result-block:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.result-giga {
  border-left-color: #667eea;
}

.result-proxy {
  border-left-color: #764ba2;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  border-bottom: 1px solid #eee;
  padding-bottom: 12px;
}

.result-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.result-content {
  min-height: 100px;
}

.result-text {
  line-height: 1.6;
  color: #555;
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* Сообщение об ошибке */
.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 12px 16px;
  border-radius: 4px;
  border-left: 3px solid #c62828;
  margin-top: 12px;
  font-size: 14px;
}

/* Информационное сообщение */
.info-message {
  background-color: #e3f2fd;
  color: #1565c0;
  padding: 12px 16px;
  border-radius: 4px;
  border-left: 3px solid #1565c0;
  margin-top: 16px;
  font-size: 14px;
}

/* Успешное сообщение */
.success-message {
  background-color: #e8f5e9;
  color: #2e7d32;
  padding: 12px 16px;
  border-radius: 4px;
  border-left: 3px solid #2e7d32;
}
```

---

## JavaScript код

### Основные функции

```javascript
/**
 * Анализирует таблицу через AI API
 */
async function analyzeTable() {
  try {
    // Получаем количество строк
    const rowsCount = parseInt(
      document.getElementById('rows-count').value || 15
    );
    
    // Валидация
    if (rowsCount < 1 || rowsCount > 100) {
      showError('Количество строк должно быть от 1 до 100');
      return;
    }
    
    // Показываем спиннер
    showLoading(true);
    
    // Отправляем запрос
    console.log(`Отправляю запрос анализа для ${rowsCount} строк...`);
    
    const response = await fetch('/api/table-analysis', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ rows_count: rowsCount })
    });
    
    const data = await response.json();
    
    // Обрабатываем ответ
    if (data.status === 'success') {
      displayResults(data);
    } else {
      showError(data.message || 'Ошибка при анализе таблицы');
    }
    
  } catch (error) {
    console.error('Ошибка:', error);
    showError(`Ошибка при отправке запроса: ${error.message}`);
  } finally {
    showLoading(false);
  }
}

/**
 * Отображает результаты анализа
 */
function displayResults(data) {
  // Показываем контейнер результатов
  document.getElementById('analysis-results').style.display = 'grid';
  
  // GigaChat результат
  const gigaElement = document.getElementById('giga-result');
  const gigaErrorElement = document.getElementById('giga-error');
  
  if (data.giga_result) {
    gigaElement.textContent = data.giga_result;
    gigaErrorElement.style.display = 'none';
  } else if (data.errors.giga_chat) {
    gigaElement.textContent = '';
    gigaErrorElement.textContent = '❌ Ошибка: ' + data.errors.giga_chat;
    gigaErrorElement.style.display = 'block';
  }
  
  // Proxy API результат
  const proxyElement = document.getElementById('proxy-result');
  const proxyErrorElement = document.getElementById('proxy-error');
  
  if (data.proxy_result) {
    proxyElement.textContent = data.proxy_result;
    proxyErrorElement.style.display = 'none';
  } else if (data.errors.proxy_api) {
    proxyElement.textContent = '';
    proxyErrorElement.textContent = '❌ Ошибка: ' + data.errors.proxy_api;
    proxyErrorElement.style.display = 'block';
  }
  
  // Показываем успешное сообщение
  if (data.giga_result || data.proxy_result) {
    showSuccess('Анализ успешно завершен!');
  }
}

/**
 * Показывает/скрывает индикатор загрузки
 */
function showLoading(show) {
  const loadingElement = document.getElementById('loading-indicator');
  const analyzeBtn = document.getElementById('analyze-btn');
  
  if (show) {
    loadingElement.style.display = 'flex';
    analyzeBtn.disabled = true;
    document.getElementById('analysis-results').style.display = 'none';
  } else {
    loadingElement.style.display = 'none';
    analyzeBtn.disabled = false;
  }
}

/**
 * Показывает сообщение об ошибке
 */
function showError(message) {
  const infoElement = document.getElementById('info-message');
  infoElement.className = 'error-message';
  infoElement.textContent = '❌ ' + message;
  infoElement.style.display = 'block';
  
  setTimeout(() => {
    infoElement.style.display = 'none';
  }, 5000);
}

/**
 * Показывает успешное сообщение
 */
function showSuccess(message) {
  const infoElement = document.getElementById('info-message');
  infoElement.className = 'success-message';
  infoElement.textContent = '✅ ' + message;
  infoElement.style.display = 'block';
  
  setTimeout(() => {
    infoElement.style.display = 'none';
  }, 3000);
}

/**
 * Копирует результат в буфер обмена
 */
function copyToClipboard(type) {
  let text = '';
  
  if (type === 'giga') {
    text = document.getElementById('giga-result').textContent;
  } else if (type === 'proxy') {
    text = document.getElementById('proxy-result').textContent;
  }
  
  if (!text) {
    showError('Нечего копировать');
    return;
  }
  
  navigator.clipboard.writeText(text).then(() => {
    showSuccess('Результат скопирован в буфер обмена');
  }).catch(() => {
    showError('Ошибка при копировании');
  });
}

/**
 * Очищает результаты анализа
 */
function resetAnalysis() {
  document.getElementById('analysis-results').style.display = 'none';
  document.getElementById('giga-result').textContent = '';
  document.getElementById('proxy-result').textContent = '';
  document.getElementById('giga-error').style.display = 'none';
  document.getElementById('proxy-error').style.display = 'none';
  document.getElementById('rows-count').value = '15';
}
```

---

## Полный пример

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DataAnalytics - Анализ таблиц</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #f5f5f5;
      padding: 20px;
    }
    
    .container {
      max-width: 1200px;
      margin: 0 auto;
    }
    
    .header {
      text-align: center;
      margin-bottom: 40px;
    }
    
    .header h1 {
      font-size: 48px;
      color: #333;
      margin-bottom: 10px;
    }
    
    .header p {
      font-size: 16px;
      color: #666;
    }
    
    /* [Вставьте CSS стили из раздела выше] */
    
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📊 DataAnalytics</h1>
      <p>Анализ таблиц через искусственный интеллект</p>
    </div>
    
    <!-- Основная панель анализа -->
    <div class="analysis-panel">
      <h2>📊 AI Анализ таблицы</h2>
      
      <div class="analysis-controls">
        <div class="control-group">
          <label for="rows-count">Количество строк:</label>
          <input type="number" 
                 id="rows-count" 
                 value="15" 
                 min="1" 
                 max="100">
        </div>
        
        <div class="control-buttons">
          <button id="analyze-btn" class="btn btn-primary" onclick="analyzeTable()">
            <span class="btn-icon">🚀</span>
            Анализировать
          </button>
          
          <button id="reset-btn" class="btn btn-secondary" onclick="resetAnalysis()">
            <span class="btn-icon">🔄</span>
            Очистить
          </button>
        </div>
      </div>
      
      <div id="loading-indicator" class="loading-indicator" style="display: none;">
        <div class="spinner"></div>
        <p>Анализируем данные...</p>
      </div>
      
      <div id="analysis-results" class="analysis-results" style="display: none;">
        <div class="result-block result-giga">
          <div class="result-header">
            <h3>📊 Анализ GigaChat</h3>
            <button class="btn-copy" onclick="copyToClipboard('giga')">
              📋 Копировать
            </button>
          </div>
          <div class="result-content">
            <p id="giga-result" class="result-text">Ожидание результата...</p>
            <div id="giga-error" class="error-message" style="display: none;"></div>
          </div>
        </div>
        
        <div class="result-block result-proxy">
          <div class="result-header">
            <h3>🤖 Анализ Proxy API</h3>
            <button class="btn-copy" onclick="copyToClipboard('proxy')">
              📋 Копировать
            </button>
          </div>
          <div class="result-content">
            <p id="proxy-result" class="result-text">Ожидание результата...</p>
            <div id="proxy-error" class="error-message" style="display: none;"></div>
          </div>
        </div>
      </div>
      
      <div id="info-message" class="info-message" style="display: none;"></div>
    </div>
  </div>
  
  <script>
    // [Вставьте JavaScript код из раздела выше]
  </script>
</body>
</html>
```

---

## Интеграция в существующую структуру

### В templates/index.html

Добавьте перед закрывающим тегом `</body>`:

```html
<!-- AI Analysis Panel -->
<div id="ai-analysis-section" style="display: none;">
  <div class="analysis-panel">
    <h2>📊 AI Анализ таблицы</h2>
    
    <div class="analysis-controls">
      <div class="control-group">
        <label for="rows-count">Количество строк:</label>
        <input type="number" id="rows-count" value="15" min="1" max="100">
      </div>
      
      <div class="control-buttons">
        <button class="btn btn-primary" onclick="analyzeTable()">
          🚀 Анализировать
        </button>
      </div>
    </div>
    
    <div id="loading-indicator" style="display: none;">
      <div class="spinner"></div>
      <p>Анализируем...</p>
    </div>
    
    <div id="analysis-results" style="display: none;">
      <div class="result-block">
        <h3>GigaChat</h3>
        <p id="giga-result"></p>
      </div>
      <div class="result-block">
        <h3>Proxy API</h3>
        <p id="proxy-result"></p>
      </div>
    </div>
  </div>
</div>

<script>
  // Показываем панель анализа когда загружены данные
  function onDataLoaded() {
    const section = document.getElementById('ai-analysis-section');
    if (section) {
      section.style.display = 'block';
    }
  }
  
  // Остальной JavaScript код...
</script>
```

---

## ✅ Чек-лист интеграции

- [ ] Скопирована HTML разметка
- [ ] Добавлены CSS стили
- [ ] Добавлен JavaScript код
- [ ] Протестирована функция анализа
- [ ] Проверены ошибки в консоли
- [ ] Проверена мобильная адаптивность
- [ ] Проверена доступность (a11y)
- [ ] Добавлены иконки и визуальные элементы

---

**Готово! Теперь ваш фронтенд имеет полную интеграцию анализа таблиц через AI! 🎉**
