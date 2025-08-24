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

// Handle dynamic performer fields
$(document).ready(function() {
    // Add performer
    $('#add-performer').click(function() {
        var performerCount = $('#performers-container .performer-entry').length;
        var template = $('#performers-container .performer-entry:first').clone();
        
        // Update the form field names
        template.find('input, select').each(function() {
            var oldName = $(this).attr('name');
            if (oldName) {
                var newName = oldName.replace('-0-', '-' + performerCount + '-');
                $(this).attr('name', newName);
            }
        });
        
        // Clear the values
        template.find('input[type="checkbox"]').prop('checked', false);
        template.find('select').prop('selectedIndex', 0);
        
        $('#performers-container').append(template);
    });
    
    // Remove performer
    $(document).on('click', '.remove-performer', function() {
        if ($('#performers-container .performer-entry').length > 1) {
            $(this).closest('.performer-entry').remove();
            
            // Update indices for remaining performers
            $('#performers-container .performer-entry').each(function(index) {
                $(this).find('input, select').each(function() {
                    var oldName = $(this).attr('name');
                    if (oldName) {
                        var newName = oldName.replace(/performers-\d+-/, 'performers-' + index + '-');
                        $(this).attr('name', newName);
                    }
                });
            });
        }
    });
    
    // Handle dynamic producer fields
    $('#add-producer').click(function() {
        var producerCount = $('#producers-container .producer-entry').length;
        var template = $('#producers-container .producer-entry:first').clone();
        
        // Update the form field names
        template.find('input, select').each(function() {
            var oldName = $(this).attr('name');
            if (oldName) {
                var newName = oldName.replace('-0-', '-' + producerCount + '-');
                $(this).attr('name', newName);
            }
        });
        
        // Clear the values
        template.find('input[type="checkbox"]').prop('checked', false);
        template.find('select').prop('selectedIndex', 0);
        
        $('#producers-container').append(template);
    });
    
    // Remove producer
    $(document).on('click', '.remove-producer', function() {
        if ($('#producers-container .producer-entry').length > 1) {
            $(this).closest('.producer-entry').remove();
            
            // Update indices for remaining producers
            $('#producers-container .producer-entry').each(function(index) {
                $(this).find('input, select').each(function() {
                    var oldName = $(this).attr('name');
                    if (oldName) {
                        var newName = oldName.replace(/producers-\d+-/, 'producers-' + index + '-');
                        $(this).attr('name', newName);
                    }
                });
            });
        }
    });
    
    // Handle dynamic film fixation producer fields
    $('#add-film-fixation-producer').click(function() {
        var producerCount = $('#film-fixation-producers-container .film-fixation-producer-entry').length;
        var template = $('#film-fixation-producers-container .film-fixation-producer-entry:first').clone();
        
        // Update the form field names
        template.find('input, select').each(function() {
            var oldName = $(this).attr('name');
            if (oldName) {
                var newName = oldName.replace('-0-', '-' + producerCount + '-');
                $(this).attr('name', newName);
            }
        });
        
        // Clear the values
        template.find('input[type="checkbox"]').prop('checked', false);
        template.find('select').prop('selectedIndex', 0);
        
        $('#film-fixation-producers-container').append(template);
    });
    
    // Remove film fixation producer
    $(document).on('click', '.remove-film-fixation-producer', function() {
        if ($('#film-fixation-producers-container .film-fixation-producer-entry').length > 1) {
            $(this).closest('.film-fixation-producer-entry').remove();
            
            // Update indices for remaining producers
            $('#film-fixation-producers-container .film-fixation-producer-entry').each(function(index) {
                $(this).find('input, select').each(function() {
                    var oldName = $(this).attr('name');
                    if (oldName) {
                        var newName = oldName.replace(/film_fixation_producers-\d+-/, 'film_fixation_producers-' + index + '-');
                        $(this).attr('name', newName);
                    }
                });
            });
        }
    });
}); 