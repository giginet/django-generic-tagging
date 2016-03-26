$(function() {
    'use strict'
    var $containers = $(".generic-tagging-container");
    $containers.each(function() {
        var $tagList = $(this).find('.tag-list');
        var $tagTemplate = $(this).find('.tag');
        var objectID = $(this).data('object-id');
        var contentType = $(this).data('content-type');

        $tagTemplate.remove();
        var $list = $(this).find('.tag-list');
        var listAPIEndpoint = $list.data('tag-list-api');

        function addTag(item, animation) {
            var $newTag = $tagTemplate.clone();
            var $link = $newTag.find('a.tag-link');
            $link.text(item['tag']['label']);
            $link.attr('href', item['tag']['absolute_url']);
            $tagList.append($newTag);
            if (animation) {
                $newTag.fadeOut(0);
                $newTag.fadeIn('slow');
            }
        }

        // retrieve
        $.when($.get(listAPIEndpoint, {'object_id': objectID, 'content_type': contentType}))
            .done(function(tags) {
                tags.forEach(function(item) {
                    addTag(item);
                });
            })
            .fail(function(e) {
                alert(e['responseText']);
            });

        // create
        var $form = $(this).find('form');
        $form.on('submit', function(e) {
            e.preventDefault();
            var endpoint = $form.attr('action');
            var params = $form.serializeArray();
            $.when($.post(endpoint, params))
                .done(function(item) {
                    $form.find("[name='tag']").val('');
                    addTag(item, true);
                })
                .fail(function(e) {
                    alert(e['responseText']);
                });
           return false;
        });

        //delete
        $tagList.delegate('.delete-button',
            'click',
            function(e) {
                e.preventDefault();
                if (confirm("Are you sure to delete this tag?")) {
                    var $tag = $(this).closest('li.tag');
                    var deleteEndPoint = $(this).attr('href');
                    $.when($.ajax({'method': 'DELETE', 'url': deleteEndPoint}))
                        .done(function(response) {
                            $tag.fadeOut('slow', function() {
                                $(this).remove();
                            });
                        })
                        .fail(function(response) {

                        });
                }
                return false;
        });
    });
});
