$(document).ready(function() {
    // on render
    $('#preview').hide();
    $('#confirm').hide();

    // On file select, show the preview button
    $('#file-input').change(function(){
        $('#preview').show();
    });

    // show preview of judges to be uploaded
    $('#preview').click(function(){
        var file = $('#file-input')[0].files[0];
        if(file) {
            readFile(file);
            // onload preview is triggered
        }
    });

    function readFile(file) {
        var reader = new FileReader();
        reader.readAsText(file, "UTF-8");

        // check reading progress
        // reader.onprogress = updateProgress;
        reader.onload = loaded;
        reader.onerror = errorHandler;
    }

//    function updateProgress(evt) {
//        if (evt.lengthComputable) {
//            // evt.loaded and evt.total are ProgressEvent properties
//            var loaded = (evt.loaded / evt.total);
//            if (loaded < 1) {
//                // Increase the prog bar length
//                // style.width = (loaded * 200) + "px";
//            }
//        }
//    }

    function loaded(event) {
        // Obtain the read file data, trigger preview
        preview(event.target.result);
    }

    function errorHandler(event) {
         if(evt.target.error.name == "NotReadableError") {
             console.log("file input could not be read");
        }
    }

    // TODO: Expand later so there is preview and confirm
    // TODO: Add more error checking
    function preview(data) {
        var arr = parseCSV(data);
        console.log(arr);
    }

    function parseCSV(data) {
        data = data.split(/\n/);
        data.forEach(function(line, index) {
            this[index] = line.split(/,/);
        }, data);
        return data;
    }

});