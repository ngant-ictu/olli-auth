
$(document).ready(function() {
    // create highlight area
    var sandbox = document.getElementById('annotation-wrapper');

    var hltr = new TextHighlighter(sandbox, {
        onBeforeHighlight: function (range) {
            Tipped.remove('.highlighted');

            return true;
        },
        onAfterHighlight: function (range, highlights) {
            var selectedText = $(highlights).text();

            // create pop-up
            var tooltip = Tipped.create(highlights, function(ele) {
                var popupBox = $('.tool-tip').comments().html();
                var hlId = $(highlights).attr('data-timestamp');

                // prepare content for popup, send required highlight data
                popupBox = popupBox.replace('###highlight-id###', hlId);
                popupBox = popupBox.replace('###highlight-text###', selectedText);

                return popupBox;
            }, {
                close: true,
                hideOn: false,
                position: 'bottom'
            });

            // show popup
            tooltip.tooltips[0].show();

            // margin Left if has space at the start of phase
            if (selectedText.indexOf(' ') === 0) {
                $(highlights).css('margin-left', '5px');
            }

            // margin Right if has space at the end of phase
            if (selectedText.indexOf(' ', selectedText.length - 1) !== -1) {
                $(highlights).css('margin-right', '5px');
            }
        }
    });

    // set default color for hl element
    hltr.setColor('#fff');

    // remove speech record
    $(".remove-speech").inlineConfirmation({
        confirm: "<a href='#' class='confirm-yes'>Yes</a>",
        cancel: "<a href='#' class='confirm-no'>No</a>",
        separator: " | ",
        confirmCallback: function(ele) {
            var recordTextEle = $(ele).parent().parent().parent();

            // send ajax remove Speech record
            $.ajax({
                cache: false,
                method: 'POST',
                url: '/admin/annotation/deletespeech',
                dataType: 'json',
                data: {
                    fid: recordTextEle.data('id')
                },
                complete: function(response, textStatus, errorThrown) {
                    if (textStatus == 'error') {
                        toastr.error('Delete causing problem. Try again later!', 'Intent SPEECH');
                    } else {
                        toastr.success('Delete OK!', 'Intent SPEECH');

                        recordTextEle.slideUp('slow', function() {
                            recordTextEle.remove();
                        });
                    }
                }
            });
        }
    });

    // reset speech record
    $(".reset-speech").on('click', function() {
        var recordTextEle = $(this).parent().parent().parent();
        var speechId = recordTextEle.data('id');
        var textOrigin = recordTextEle.data('origin');
        var lineText = recordTextEle.find('.line').text();

        // send ajax reset Speech record
        $.ajax({
            cache: false,
            method: 'POST',
            url: '/admin/annotation/resetspeech',
            dataType: 'json',
            data: {
                fid: speechId
            },
            complete: function(response, textStatus, errorThrown) {
                if (textStatus == 'error') {
                    toastr.error('Reset problem. Try again later!', 'Intent SPEECH');
                } else {
                    toastr.success('Reset OK!', 'Intent SPEECH');
                    // remove all content before .tools class
                    recordTextEle.find('.line').remove();
                    recordTextEle.find('.highlighted').remove();
                    recordTextEle.contents().each(function(){
                        if (this.nodeType === 3) {
                            $(this).remove();
                        }
                    });

                    var htmlString = '<span class="line disable-select">'+ lineText +'</span>';
                        htmlString += response.responseJSON.stringHtml.content;

                    recordTextEle.prepend(htmlString);
                }
            }
        });
    });
});

// remove existed highlight slot
function removeHighlight(slotId) {
    // send ajax remove slot
    $.ajax({
        cache: false,
        method: 'POST',
        url: '/admin/annotation/deleteslot',
        dataType: 'json',
        data: {
            fid: slotId
        },
        complete: function(response, textStatus, errorThrown) {
            if (textStatus == 'error') {
                toastr.error('Delete causing problem. Try again later!', 'Intent SLOT');
            } else {
                var hlElement = $('.highlighted[data-id="'+ slotId +'"]');
                toastr.success('Delete OK!', 'Intent SLOT');
                hlElement.slideUp('slow', function() {
                    hlElement.replaceWith(response.responseJSON.text);
                });

            }
        }
    });
}
