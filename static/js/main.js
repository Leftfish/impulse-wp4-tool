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

let textReport = ''; // Store the text report in a variable

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
            textReport = response.text;
        }
    });
});

// Handle the download report button
$('#download-report').click(function() {
    downloadReport(textReport);
}); 