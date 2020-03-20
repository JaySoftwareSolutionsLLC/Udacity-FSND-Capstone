/* General CRUD process using modals

1) User clicks on a CRUD icon (plus, pencil, trash)
2) Ajax call goes to request_form_data route with request specifics
    (object="Category", "Topic", or "Concept",
     type="Update" or "Create",
     id if this is an edit or delete function)
3) Route responds with a template based on request
4) Use jQuery to populate modal div with response (html of form)
5) User fills out modal form as desired
6) User submits the form
7) Ajax call to route from form action
8) Endpoint will respond with json object
8) Update DOM to reflect changes (using jQuery) or show red X if CRUD request failed

References:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
https://mrl33h.de/post/21

*/

// Takes in a singular string and returns the plural of that string
function pluralize(string) {
    switch (string) {
        case 'category':
            pluralStr = 'categories';
            break;
    
        default:
            pluralStr = string + 's';
            break;
    }
    return pluralStr;
}

// CRUD event listener
function openModalFromCRUDIconClick() {
    $('i.fa-plus, i.fa-pencil-alt').on('click', function(e) {
        // Prevent following url or other events as result of clicking on element
        e.preventDefault();
        e.stopPropagation();
        let iconEl = $(this);
        // Specify variables
        let model = $(this).attr('data-model');
        let id = $(this).attr('data-id') || 0;
        let parentId = $(this).attr('data-parent-id') || 0;
        let formType = '';
        if (iconEl.hasClass('fa-plus')) {
            formType = 'create';
        }
        if (iconEl.hasClass('fa-pencil-alt')) {
            formType = 'update';
        }
        console.log(`requesting form to ${formType} ${model}`)
        // Request appropriate form html from endpoint 
        $.ajax({
            type: "post",
            url: "/request_form_data",
            data: JSON.stringify({
                model: model,
                formType: formType,
                id: id,
                parentId: parentId
            }),
            contentType: 'application/json', // request = JSON
            dataType: 'html', // response = HTML
            success: function (response) {
                console.log(response);
                let modalEl = $('div#modal');
                // Delete all content in modal and replace with form
                modalEl.empty().html(response);
                modalEl.css('display', 'flex');
                listenForModalClose();
                listenForModalFormSubmission(model, id);
                listenForObjectDeletion(model, id);
            }
        });
    });
}

// If user clicks on modal's "X" icon then modal should be emptied and closed
function listenForModalClose() {
    $('i.fa-times').on('click', function() {
        $('div#modal').empty().css('display', 'none');
    })
}

(function ($) {
    $.fn.serializeAll = function () {
        var data = $(this).serializeArray();

        $(':disabled[name]', this).each(function () { 
            data.push({ name: this.name, value: $(this).val() });
        });

        return data;
    }
})(jQuery);

// Upon submission of form by user, request that the db be updated
// ...with either the creation of a new row or the modification of
// ...fields within a currently existing row
function listenForModalFormSubmission(model, id) {
    $('div#modal form input#submit').on('click', function(e) {
        // Prevent default behavior (form submission)
        e.preventDefault();
        let formEl = $('div#modal form');
        // Save relevant info for request as variables
        let token = localStorage.getItem('jwt');
        let url = formEl.attr('action');
        let method = formEl.attr('method');
        let data = formEl.serializeAll();
        let jsonData = {}
        data.forEach(e => {
            if (e['name'] != 'csrf_token') {
                jsonData[e['name']] = e['value'];
            }
        });
        console.log(`Sending a request to ${url} with data:`);
        console.log(jsonData);
        $.ajax({
            type: method,
            url: url,
            data: JSON.stringify(jsonData),
            contentType: 'application/json', // request = JSON
            dataType: "json", // response = JSON
            // CRUD endpoints require appropriate authorization
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            success: function (responseJSON) {
                console.log(responseJSON)
                if (responseJSON.success) {
                    // Empty & hide modal
                    $('div#modal').empty().css('display', 'none');

                    // Remove old representation from DOM if it exists
                    removeObjectFromDOM(model, id)

                    // Create new element to represent new/modified object
                    let parentId = responseJSON[model]['topic_id'] ||
                                   responseJSON[model]['category_id'] ||
                                   0
                    addObjectToDOM(model, parentId, responseJSON[model]['html'])

                    // Reset listeners for CRUD icons
                    openModalFromCRUDIconClick();
                }
            }
        });
    });
}

// Delete functionality occurs within form by clicking on trash icon
function listenForObjectDeletion(model, id) {
    $('form i.fa-trash').on('click', function() {
        let confirmed = confirm(`Are you sure you want to delete this ${model}`);
        if (confirmed) {
            let modelPlural = pluralize(model)
            $.ajax({
                type: 'delete',
                url: `/api/${modelPlural}/${id}`,
                dataType: "json",
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                success: function (responseJSON) {
                    console.log(responseJSON)
                    if (responseJSON.success) {
                        $('div#modal').empty().css('display', 'none');
                        removeObjectFromDOM(model, id)
                    }
                }
            });
        }
    })
}

// function replaceObjectFromDOM() {

// }

function removeObjectFromDOM(model, id) {
    // Will need to update from just links (<a>) to include divs/spans for topics & concepts
    $('a, ul, li').each(function() {
        if ($(this).hasClass(model) && $(this).attr('data-id') == id) {
            $(this).remove();
        }
    })
}

function addObjectToDOM(model, parentId, html) {
    if (model == 'category') {
        $('section#categories').append(html);
        return;
    } 
    if (model == 'topic') {
        $('section#topics').append(html);
        return;
    }
    if (model == 'concept') {
        $('ul.topic').each(function() {
            if ($(this).attr('data-id') == parentId) {
                $(this).append(html);
            }
        })
    }
}

openModalFromCRUDIconClick();