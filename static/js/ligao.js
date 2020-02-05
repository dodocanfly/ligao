(function ($) {

    $("#id_category").change(function () {
        let team_form = $("#team-form-id");
        getAjaxData(team_form.data('seasons-url'), 'team_category', $(this).val(), '#id_season');
        getAjaxData(team_form.data('clubs-url'), 'team_category', $(this).val(), '#id_club');
    });

    function getAjaxData(url, dataName, dataVal, targetId, value='id', label='name') {
        let dataArray = {};
        dataArray[dataName] = dataVal;
        $.ajax({
            url: url,
            data: dataArray,
            success: function (data) {
                let htmloptions = renderOptions(data, value, label);
                let htmloptions2 = $(targetId).html().replace(/\>\s+\</g,'><').replace(' selected=""', '').trim();
                if (htmloptions !== htmloptions2) {
                    $(targetId).html(htmloptions);
                }
            }
        });
    }

    function renderOptions(data, value='id', label='name') {
        let html = '<option value="">---------</option>';
        if (data.length > 0) {
            for (let item of data) {
                html += '<option value="' + item[value] + '">' + item[label] + '</option>';
            }
        }
        return html;
    }

})(jQuery);
