$(document).ready(function() {
    // on render hide both buttons
    $('#preview').hide();
    $('#confirm').hide();

    // cross site request forgery prevention
    var csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

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

    // POST data on confirm button
    $('#confirm').click(function(){
        console.log(window.judge_info);

        $.ajax({
            type: "POST",
            url: "/admin/judges/judge-upload/",
            data: {
                "judge_info": JSON.stringify(window.judge_info),
            },
            success: function(data){
                console.log("Success");
                $('#confirm').hide();
                $( "#message" ).append( "<h2>Judges successfully added. :)</h2>" );
            },
            failure: function(){
                console.log("Failure");
                console.log(window.judge_info);
                $( "#message" ).append( "<h2>Judges could not be added. :(</h2>" );
            },
        });
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
        // Obtain the read file data, trigger preview; switch buttons
        preview(event.target.result);
        $('#preview').hide();
        $('#confirm').show();
    }

    function errorHandler(event) {
         if(evt.target.error.name == "NotReadableError") {
             console.log("file input could not be read");
        }
    }

    // TODO: Expand later so there is actually a preview
    // TODO: Add more error checking
    function preview(data) {
        window.judge_info = parseCSV(data);;
    }

    function parseCSV(data) {
        data = data.split(/\r\n/);
        data.forEach(function(line, index) {
            this[index] = line.split(/,/);
        }, data);
        // cut our header row and empty last row
        data = data.slice(1, -1);
        return data;
    }
});