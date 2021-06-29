let customUpload = $('.files-upload')
customUpload.on('click', function() {
    $('input[name="poster"]').click()
})

$('input[name="poster"]').on('change', function() {
    previewImg()
})

$('.remove').on('click', function() {
    remove()
})

function previewImg(){
    let fileInput = document.getElementsByName('poster')[0].value
    let file = fileInput.files
    let reader = new FileReader()

    reader.onload = function (e) {
        let img = $('.poster')
        if (img) {
            img.attr('src', e.target.result);
        }
    }

    if (file && file[0]) {
        reader.readAsDataURL(file[0]);
    }

    if (fileInput.files.length > 0){
        let fileName = fileInput.value.split('\\')
        $('.filename').html(fileName[fileName.length - 1])
        $('.infos').removeClass('d-none')
        $('.remove').removeClass('d-none')
        $('.card-text').addClass('d-none')
    }
    else{
        $('.infos').addClass('d-none')
        $('.remove').addClass('d-none')
        $('.card-text').removeClass('d-none')
    }
}

function removeFile(){
    $('.infos').addClass('d-none')
    $('.remove').addClass('d-none')
    $('.card-text').removeClass('d-none')
    $('input[name="poster"]').val('')
    $('.poster').src('{{ url_for("static", filename="/img/placeholder.jpg") }}')
}
