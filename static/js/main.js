// Function to download the report as Markdown
function downloadReport(content) {
    const element = document.createElement('a');
    const file = new Blob([content], {type: 'text/markdown'});
    element.href = URL.createObjectURL(file);
    element.download = 'copyright-evaluation-report.md';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// Handle form reset on page refresh
window.onload = function() {
    document.getElementById('copyright-form').reset();
    document.getElementById('result').style.display = 'none';
};

// Handle the download report button
document.getElementById('download-report').addEventListener('click', function() {
    const resultContent = document.getElementById('result-content').textContent;
    downloadReport(resultContent);
}); 