var script = document.createElement('script');
script.type = 'text/javascript';
script.src = "https://cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js";
document.head.appendChild(script);
script.onload = function () {
    tinymce.init({
        selector: '#id_content',
<<<<<<< HEAD
        width: 100,
=======
        width: 500,
>>>>>>> ea2ff61d147db05577e052d7159c74a11000e594
        height: 300,
        plugins: [
            'advlist autolink link image imagetools lists charmap print preview hr anchor pagebreak',
            'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
            'table emoticons template paste help'
        ],
        toolbar: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | ' +
            'bullist numlist outdent indent | link image | print preview media fullpage | ' +
            'forecolor backcolor emoticons | help | image',
        imagetools_toolbar: "rotateleft rotateright | flipv fliph | editimage imageoptions",
        image_title: true,
        automatic_upload: true,
        file_picker_types: 'image',
        file_picker_callback: function(cb, value, meta) {
            var input = document.createElement('input');
            input.setAttribute('type', 'file');
            input.setAttribute('accept', 'image/*');
            input.onchange = function() {
                var file = this.files[0];
                var reader = new FileReader();
                reader.onload = function() {
                    var id = 'blobid' + (new Date()).getTime();
                    var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                    var base64 = reader.result.split(',')[1];
                    var blobInfo = blobCache.create(id, file, base64);
                    blobCache.add(blobInfo);
                    cb(blobInfo.blobUri(), {title: file.name});
                };
                reader.readAsDataURL(file);
            };
            input.click();
        },
        menu: {
            favs: { title: 'My Favorites', items: 'code visualaid | searchreplace | emoticons' }
        },
        menubar: 'favs file edit view insert format tools table help',
        // content_css: 'css/content.css'
        // images_upload_url: '/static/',
        // images_upload_handler: function (blobInfo, success, failure, progress) {
        //     var xhr, formData;
        
        //     xhr = new XMLHttpRequest();
        //     xhr.withCredentials = false;
        //     xhr.open('POST', 'postAcceptor.php');
        
        //     xhr.upload.onprogress = function (e) {
        //       progress(e.loaded / e.total * 100);
        //     };
        
        //     xhr.onload = function() {
        //       var json;
        
        //       if (xhr.status < 200 || xhr.status >= 300) {
        //         failure('HTTP Error: ' + xhr.status);
        //         return;
        //       }
        
        //       json = JSON.parse(xhr.responseText);
        
        //       if (!json || typeof json.location != 'string') {
        //         failure('Invalid JSON: ' + xhr.responseText);
        //         return;
        //       }
        
        //       success(json.location);
        //     };
        
        //     xhr.onerror = function () {
        //       failure('Image upload failed due to a XHR Transport error. Code: ' + xhr.status);
        //     };
        
        //     formData = new FormData();
        //     formData.append('file', blobInfo.blob(), blobInfo.filename());
        
        //     xhr.send(formData);
        //   }
    });
}
