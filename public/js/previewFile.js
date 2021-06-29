let customUpload = $('.wrapper')
customUpload.on('click', function() {
    customUpload.closest('.files-upload').find('input[name="poster"]').click()
})

$('input[name="poster"]').on('change', function() {
    previewImg()
})

$('.remove').on('click', function() {
    removeFile()
})

function previewImg(){
    let fileInput = document.getElementsByName('poster')[0]
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

    if (file.length > 0){
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
        $('.poster').attr('src', '/public/img/placeholder.jpg')
    }
}

function removeFile(){
    $('.infos').addClass('d-none')
    $('.remove').addClass('d-none')
    $('.card-text').removeClass('d-none')
    $('input[name="poster"]').val('')
    $('.poster').attr('src', '/public/img/placeholder.jpg')
}
