// Function to download the report as text
function downloadReport(content) {
    const element = document.createElement('a');
    const file = new Blob([content], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);

    // Build dynamic filename: legal_status_report_[slug_]YYYYMMDD_HHMM.txt
    const baseName = 'legal_status_report';

    let slug = '';
    const objectNameInput = document.getElementById('object_name');
    if (objectNameInput && objectNameInput.value) {
        const lettersAndDigitsOnly = objectNameInput.value.toLowerCase().replace(/[^a-z0-9]+/g, '');
        if (lettersAndDigitsOnly.length > 0) {
            slug = lettersAndDigitsOnly.slice(0, 8);
        }
    }

    const now = new Date();
    const yyyy = String(now.getFullYear());
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const dd = String(now.getDate()).padStart(2, '0');
    const HH = String(now.getHours()).padStart(2, '0');
    const MM = String(now.getMinutes()).padStart(2, '0');
    const timestamp = `${yyyy}${mm}${dd}_${HH}${MM}`;

    const parts = [baseName];
    if (slug) {
        parts.push(slug);
    }
    parts.push(timestamp);
    element.download = parts.join('_') + '.txt';

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

// Handle dynamic performer fields
$(document).ready(function() {
    // Handle form submission (consolidated - displays response AND stores text for download)
    $('#copyright-form').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: '/',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                // Display the HTML response in the browser
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

    // Handle dynamic broadcaster fields
    $('#add-broadcaster').click(function() {
        var broadcasterCount = $('#broadcasters-container .broadcaster-entry').length;
        var template = $('#broadcasters-container .broadcaster-entry:first').clone();
        
        template.find('input, select').each(function() {
            var oldName = $(this).attr('name');
            if (oldName) {
                var newName = oldName.replace('-0-', '-' + broadcasterCount + '-');
                $(this).attr('name', newName);
            }
        });
        
        template.find('input[type="checkbox"]').prop('checked', false);
        template.find('select').prop('selectedIndex', 0);
        
        $('#broadcasters-container').append(template);
    });
    
    $(document).on('click', '.remove-broadcaster', function() {
        if ($('#broadcasters-container .broadcaster-entry').length > 1) {
            $(this).closest('.broadcaster-entry').remove();
            
            $('#broadcasters-container .broadcaster-entry').each(function(index) {
                $(this).find('input, select').each(function() {
                    var oldName = $(this).attr('name');
                    if (oldName) {
                        var newName = oldName.replace(/broadcasters-\d+-/, 'broadcasters-' + index + '-');
                        $(this).attr('name', newName);
                    }
                });
            });
        }
    });

    // Handle dynamic author fields
    $('#add-author').click(function() {
        var authorContainer = $('#authors-container');
        var newIndex = authorContainer.children('.author-entry').length;
        
        // Clone the first author entry
        var newAuthor = $('.author-entry:first').clone();
        
        // Update the IDs and names of the cloned elements
        newAuthor.find('input, select').each(function() {
            var oldName = $(this).attr('name');
            var oldId = $(this).attr('id');
            
            if (oldName) {
                var newName = oldName.replace('-0-', '-' + newIndex + '-');
                $(this).attr('name', newName);
            }
            if (oldId) {
                var newId = oldId.replace('-0-', '-' + newIndex + '-');
                $(this).attr('id', newId);
            }
        });
        
        // Reset the values - by default author is known (not anonymous)
        newAuthor.find('input[type="checkbox"]').prop('checked', false);
        newAuthor.find('select').prop('selectedIndex', 0);
        
        // Append to container
        authorContainer.append(newAuthor);
    });

    // Remove author
    $(document).on('click', '.remove-author', function() {
        if ($('.author-entry').length > 1) {
            $(this).closest('.author-entry').remove();
            
            // Reindex remaining authors
            $('#authors-container .author-entry').each(function(index) {
                $(this).find('input, select').each(function() {
                    var oldName = $(this).attr('name');
                    var oldId = $(this).attr('id');
                    
                    if (oldName) {
                        var newName = oldName.replace(/\d+/, index);
                        $(this).attr('name', newName);
                    }
                    if (oldId) {
                        var newId = oldId.replace(/\d+/, index);
                        $(this).attr('id', newId);
                    }
                });
            });
        }
    });

    // Handle dynamic country fields
    $('#add-country').click(function() {
        var countryContainer = $('#simultaneous-countries-container');
        var newIndex = countryContainer.children('.row').length;
        
        // Clone the first country row
        var newCountry = countryContainer.children('.row:first').clone();
        
        // Update the IDs and names
        newCountry.find('select').each(function() {
            var oldName = $(this).attr('name');
            var oldId = $(this).attr('id');
            
            if (oldName) {
                var newName = oldName.replace('-0-', '-' + newIndex + '-');
                $(this).attr('name', newName);
            }
            if (oldId) {
                var newId = oldId.replace('-0-', '-' + newIndex + '-');
                $(this).attr('id', newId);
            }
        });
        
        // Reset the values
        newCountry.find('select').prop('selectedIndex', 0);
        
        // Append to container
        countryContainer.append(newCountry);
    });

    // Remove country
    $(document).on('click', '.remove-country', function() {
        if ($('#simultaneous-countries-container .row').length > 1) {
            $(this).closest('.row').remove();
            
            // Reindex remaining countries
            $('#simultaneous-countries-container .row').each(function(index) {
                $(this).find('select').each(function() {
                    var oldName = $(this).attr('name');
                    var oldId = $(this).attr('id');
                    
                    if (oldName) {
                        var newName = oldName.replace(/\d+/, index);
                        $(this).attr('name', newName);
                    }
                    if (oldId) {
                        var newId = oldId.replace(/\d+/, index);
                        $(this).attr('id', newId);
                    }
                });
            });
        }
    });

    // Collapse/expand card bodies
    $(document).on('click', '.toggle-card', function() {
        const $card = $(this).closest('.card'); // find the parent card
        const $body = $card.children('.card-body, .collapseable'); // what to hide/show

        $body.toggle(); // toggle visibility

        // Flip the button text +/−
        if ($(this).text() === 'hide') {
            $(this).text('show');
        } else {
            $(this).text('hide');
        }
    });

    // Character counters for text areas
    // Remaining chars for restrictions notes
    const notes = document.getElementById('object_restrictions_notes');
    const remaining = document.getElementById('restr-notes-remaining');
    if (notes && remaining) {
        const max = parseInt(notes.getAttribute('maxlength') || '1000', 10);
        const update = function() {
            const used = (notes.value || '').length;
            remaining.textContent = (max - used);
        };
        notes.addEventListener('input', update);
        update();
    }

    // Remaining chars for general notes
    const genNotes = document.getElementById('general_notes');
    const genRemaining = document.getElementById('general-notes-remaining');
    if (genNotes && genRemaining) {
        const maxGen = parseInt(genNotes.getAttribute('maxlength') || '1000', 10);
        const updateGen = function() {
            const used = (genNotes.value || '').length;
            genRemaining.textContent = (maxGen - used);
        };
        genNotes.addEventListener('input', updateGen);
        updateGen();
    }
}); 