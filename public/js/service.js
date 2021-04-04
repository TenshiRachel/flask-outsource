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