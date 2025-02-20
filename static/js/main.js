document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('pdf-upload-form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const response = await fetch('/process-pdf', {
            method: 'POST',
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            // Gérer le succès
            console.log('PDF processed successfully');
        }
    });
});
