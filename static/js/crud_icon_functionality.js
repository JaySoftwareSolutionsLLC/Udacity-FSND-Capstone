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
8) Conditionally reload page (success=True) or show red X

References:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
https://mrl33h.de/post/21

*/

// Create functionality
$('i.fa-plus').on('click', function() {
    let model = $(this).attr('data-model');
    let formType = 'create';
    console.log(`requesting form to ${formType} ${model}`)
    // Request
    $.ajax({
        type: "post", // POST, GET, etc.
        url: "/request_form_data",
        data: JSON.stringify({
            model: model,
            formType: formType
        }),
        contentType: 'application/json',
        dataType: "html",
        success: function (response) {
            // console.log(response);
            let modalEl = $('div#modal');
            modalEl.empty().html(response);
            modalEl.css('display', 'flex');
            listenForModalClose();
            listenForModalFormSubmission();
        }
    });
});

// Update functionality
function listenForObjectUpdate() {
    $('i.fa-pencil-alt').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        let parentFormEl = $(this).parents('a');
        let model = $(this).attr('data-model');
        let id = $(this).attr('data-id');
        let formType = 'update';
        console.log(`requesting form to ${formType} ${model}`)
        // Request
        $.ajax({
            type: "post", // POST, GET, etc.
            url: "/request_form_data",
            data: JSON.stringify({
                model: model,
                formType: formType,
                id: id
            }),
            contentType: 'application/json',
            dataType: 'html',
            success: function (response) {
                // console.log(response);
                let modalEl = $('div#modal');
                modalEl.empty().html(response);
                modalEl.css('display', 'flex');
                listenForModalClose();
                listenForModalFormSubmission(parentFormEl);
                listenForObjectDeletion(model, id, parentFormEl);
            }
        });
    });
}

// Delete functionality occurs within form
function listenForObjectDeletion(model, id, parentFormEl) {
    $('form i.fa-trash').on('click', function() {
        let confirmed = confirm(`Are you sure you want to delete this category`);
        if (confirmed) {
            switch (model) {
                case 'category':
                    modelPlural = 'categories';
                    break;
            
                default:
                    modelPlural = model + 's';
                    break;
            }
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
                        parentFormEl.remove();
                    }
                }
            });
        }
    })
}

function listenForModalFormSubmission(parentFormEl) {
    $('div#modal form input#submit').on('click', function(e) {
        e.preventDefault();
        let formEl = $('div#modal form');
        let url = formEl.attr('action');
        let method = formEl.attr('method');
        let data = formEl.serializeArray();
        let jsonData = {}
        data.forEach(e => {
            if (e['name'] != 'csrf_token') {
                jsonData[e['name']] = e['value'];
            }
        });
        let token = localStorage.getItem('jwt');
        console.log(`Sending a request to ${url} with data:`);
        console.log(jsonData);
        $.ajax({
            type: method, // POST, GET, etc.
            url: url,
            data: JSON.stringify(jsonData), // Can also be an array { val1 : val1, val2: val2 }
            dataType: "json",
            contentType: 'application/json',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            success: function (responseJSON) {
                console.log(responseJSON)
                if (responseJSON.success) {
                    $('div#modal').empty().css('display', 'none');
                    parentFormEl.empty().html(responseJSON.category.html)
                    listenForObjectUpdate();
                }
            }
        });
    });
}

listenForObjectUpdate();

function listenForModalClose() {
    $('i.fa-times').on('click', function() {
        $('div#modal').empty().css('display', 'none');
    })
}