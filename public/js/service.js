//List service
function search() {
    let input = $('#search').val();
    let filter = input.toUpperCase();
    let cards = $('.servicecards');
    let name = $('.name');

    for (let i = 0, n = cards.length; i < n; i++) {
        let focus = $(cards[i]);
        let compare = $(name[i]).data('names');

        if (compare.toUpperCase().includes(filter)) {
            if ($(focus).hasClass('d-none')) {
                $(focus).removeClass('d-none');
                $(focus).addClass('animated faster fadeIn').one(animationEnd, function() {
                    let _this = $(this);

                    _this.removeClass('animated faster fadeIn');
                    _this.addClass('d-flex');
                });
            }
        }
        else {
            if (!$(focus).hasClass('d-none')){
                $(focus).addClass('animated faster fadeOut').one(animationEnd, function(){
                    let _this = $(this);

                    _this.removeClass('animated faster fadeOut');
                    _this.removeClass('d-flex');
                    _this.addClass('d-none');
                })
            }
        }
    }
}

$(function() {
    let searchbut = document.getElementById('searchbut');

    if (searchbut) {
        searchbut.addEventListener('click', search);
    }
});

$('select.category-select').on('change', function(e) {
    let cards = $('.servicecards');
    let category = $(this).find('option:selected').text().replace(/\s/g, '');

    for (let i = 0, n = cards.length; i < n; i++) {
        let focus = $(cards[i]);

        if (($(focus).hasClass(category) || category === "ShowAll")) {
            if ($(focus).hasClass('d-none')) {
                $(focus).removeClass('d-none');
                $(focus).addClass('animated faster fadeIn').one(animationEnd, function() {
                    let _this = $(this);

                    _this.removeClass('animated faster fadeIn');
                    _this.addClass('d-flex');
                });
            }
        }
        else {
            if (!$(focus).hasClass('d-none')){
                $(focus).addClass('animated faster fadeOut').one(animationEnd, function(){
                    let _this = $(this);

                    _this.removeClass('animated faster fadeOut');
                    _this.addClass('d-none');
                    _this.removeClass('d-flex');
                })
            }
        }
    }
});

$('select.sort-select').on('change', function(e) {
    let cards = $('.servicecards');
    let sort = $(this).find('option:selected').text();
    if (sort == "Most viewed"){
        cards.sort(function(a, b){ return $(b).data("views")-$(a).data("views")});
        $("#servcon").html(cards);
    }
    else if (sort == "Newest first"){
        cards.sort(function(a, b){ return $(b).data("date")-$(a).data("date")});
        $("#servcon").html(cards);
    }
    else if (sort == "Oldest first"){
        cards.sort(function(a, b){ return $(a).data("date")-$(b).data("date")});
        $("#servcon").html(cards);
    }
    else if (sort == "Most Popular"){
        cards.sort(function(a, b){ return $(b).data("favs")-$(a).data("favs")});
        $("#servcon").html(cards);
    }
});

function categoryCheck() {
    var categories = document.getElementsByName('categories');
    var error = document.getElementById('categoryErr');
    var button = document.getElementById('butaddService');
    var ticks = 0;

    for (var i = 0; i < categories.length; i++) {
        if (categories[i].checked == true) {
            ticks++;
        }
    }
    if (ticks == 0) {
        error.style.display = 'block';
        button.disabled = true;
    }
    else {
        error.style.display = 'none';
        button.disabled = false;
    }
}