let customUpload = $('.wrapper')

if (customUpload){
    customUpload.on('click', function() {
    customUpload.closest('.files-upload').find('input[name="poster"]').click()
    })

    let poster = $('input[name="poster"]')
    if (poster){
        poster.on('change', function() {
            previewImg(document.getElementsByName('poster')[0], $('.poster'))
        })
    }
}

customUpload = $('#inputBorder')

if (customUpload){
    customUpload.on('click', function(){
        $('#upload_banner').click()
    })
    $('input[name="upload_banner"]').on('change', function() {
        previewImg(document.getElementsByName('upload_banner')[0], $('#bannerPic'))
    })

    customUpload = $('#inputImg')
    customUpload.on('click', function() {
        $('#upload_image').click()
    })
    $('input[name="upload_image"]').on('change', function() {
        previewImg(document.getElementsByName('upload_image')[0], $('#profilePic'))
    })
}

if ($('.remove')){
    $('.remove').on('click', function() {
    removeFile()
    })
}

function previewImg(fileInput, img){
    let file = fileInput.files
    let reader = new FileReader()

    reader.onload = function (e) {
        img.attr('src', e.target.result);
    }

    if (file && file[0]) {
        reader.readAsDataURL(file[0]);
    }

    if ($('.filename')){
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
            img.attr('src', '/public/img/placeholder.jpg')
        }
    }
}

function removeFile(){
    $('.infos').addClass('d-none')
    $('.remove').addClass('d-none')
    $('.card-text').removeClass('d-none')
    $('input[name="poster"]').val('')
    $('.poster').attr('src', '/public/img/placeholder.jpg')
}
