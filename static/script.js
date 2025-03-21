document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file');
    const fileNameDisplay = document.querySelector('.file-name');

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        fileNameDisplay.textContent = file ? file.name : 'No file chosen';
    });
});