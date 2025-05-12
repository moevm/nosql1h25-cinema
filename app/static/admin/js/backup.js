document.addEventListener('DOMContentLoaded', function() {
    // Экспорт
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            window.location.href = '/api/export';
        });
    }

    // Импорт
    const importBtn = document.getElementById('importBtn');
    if (importBtn) {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '.json';
        fileInput.style.display = 'none';

        fileInput.addEventListener('change', async function(e) {
            const file = e.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch('/api/import', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (response.ok) {
                    alert(`Успешный импорт! Коллекции: ${result.collections.join(', ')}`);
                } else {
                    throw new Error(result.error || 'Неизвестная ошибка');
                }
            } catch (error) {
                alert(`Ошибка импорта: ${error.message}`);
            }
        });

        importBtn.addEventListener('click', function() {
            fileInput.click();
        });
    }
});
