(function($) {


    let formname = $('form[method=post]').first().data('formname');

    $('#id_organization').change(function () {
        switch (formname) {
            case 'xteam-category-add': updateSelectList('team-categories', 'id_parent', 'organization', this.value); break;
            case 'xteam-category-edit': updateSelectList('team-categories', 'id_parent', 'organization', this.value); break;
            case 'xseason-add':
                updateSelectList('seasons', 'id_season', 'organization', this.value);
                break;
            case 'other':
                updateSelectList('game-categories', 'id_parent', 'organization', this.value);
                updateSelectList('game-categories', 'id_category', 'organization', this.value);
                updateSelectList('teams', 'id_team', 'season', $('#id_season').val(), false);
        }
    });

    $('#id_season').change(function () {
        switch (formname) {
            case 'other':
                updateSelectList('teams', 'id_team', 'season', this.value, false);
                break;
        }
    });

    $('#id_game').change(function () {
        switch (formname) {
            case 'other':
                updateSelectList('teams', 'id_host_team', 'game', this.value);
                updateSelectList('teams', 'id_guest_team', 'game', this.value);
                break;
        }
    });


})(jQuery);


function updateSelectList(name, target, depend, value, first_blank = true, exclude = 0) {
    let url = 'http://127.0.0.1:8000/api/' + name + '/?format=json&' + depend + '=' + value;
    let dropdown = $('#' + target);
    dropdown.empty();
    $.getJSON({
        url: url
    }).done(function (data) {
        if (first_blank) dropdown.append($('<option></option>').attr('value', '').text('----------'));
        if (data.length) {
            $.each(data, function (key, entry) {
                if (entry.id != exclude) {
                    dropdown.append($('<option></option>').attr('value', entry.id).text(entry.name));
                }
            })
        }
    }).fail(function (xhr, status, error) {
        alert('blad polaczenia')
    });
}
