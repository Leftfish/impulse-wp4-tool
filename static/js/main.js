// Function to download the report as text
function downloadReport(content) {
    const element = document.createElement('a');
    const file = new Blob([content], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = 'copyright-evaluation-report.txt';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// Handle form reset on page refresh
window.onload = function() {
    document.getElementById('copyright-form').reset();
    document.getElementById('result').style.display = 'none';
};

// Handle form submission
$('#copyright-form').submit(function(e) {
    e.preventDefault();
    $.ajax({
        url: '/',
        type: 'POST',
        data: $(this).serialize(),
        success: function(response) {
            $('#result').show();
            $('#result-content').html(response.html);
            // Store the text version for download
            $('#result-content').data('text-report', response.text);
        }
    });
});

// Handle the download report button
$('#download-report').click(function() {
    const textContent = $('#result-content').data('text-report');
    downloadReport(textContent);
}); 