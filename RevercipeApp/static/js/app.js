
function toggle_favorite(recipe_id){
    $.ajax({
    url: 'ajax/toggle_favorite/',
        data : {
            'recipe_id': recipe_id
        },
        success: function () {
            window.location.reload();
        }
    });
}

function toggle_profile_favorite(instance_id, recipe_id){
    $.ajax({
    url: `/ajax/toggle_favorite/`,
        data : {
            'recipe_id': recipe_id
        },
        success: function () {
            window.location.reload();
        }
    });
}
