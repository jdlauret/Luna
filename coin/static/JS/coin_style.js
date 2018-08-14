$('#note').keyup(function () {
    max = this.getAttribute("maxlength");
    var len = $(this).val().length;
    if (len >= max) {
        $('#charNum').text(' you have reached the limit');
    } else {
        var char = max - len;
        $('#charNum').text(char + ' characters left');
    }
});

function removeSpaces(string) {
    return string.split(' ').join('');
}

function openCoinTab(evt, name) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(name).style.display = "block";
    evt.currentTarget.className += " active";
}

// function textCounter(field,field2,maxlimit)
// {
//  var countfield = document.getElementById(field2);
//  if ( field.value.length > maxlimit ) {
//   field.value = field.value.substring( 0, maxlimit );
//   return false;
//  } else {
//   countfield.value = maxlimit - field.value.length;
//  }
// }

$(function () {
    // Initializes and creates emoji set from sprite sheet
    window.emojiPicker = new EmojiPicker({
        emojiable_selector: '[data-emojiable=true]',
        assetsPath: '../static/Pictures/',
        popupButtonClasses: 'fa fa-smile-o'
    });
    // Finds all elements with `emojiable_selector` and converts them to rich emoji input fields
    // You may want to delay this step if you have dynamically created input fields that appear later in the loading process
    // It can be called as many times as necessary; previously converted input fields will not be converted again
    window.emojiPicker.discover();
});

function unicodeLength(s) {
    var res = 0, count = 0, len = s.length, val, next;
    while (count < len) {
        val = s.charCodeAt(count++);
        if ((val >= 0xd800) && (val <= 0xdbff) && (count < len)) {
            next = s.charCodeAt(count++);
            if ((next & 0xFC00) != 0xDC00) count--;
        }
        res++;
    }
    return res;
}

function unicodeSplit(s) {
    var res = [], count = 0, len = s.length, val, next;
    while (count < len) {
        val = s.charCodeAt(count++);
        if ((val >= 0xd800) && (val <= 0xdbff) && (count < len)) {
            next = s.charCodeAt(count++);
            if ((next & 0xFC00) == 0xDC00) {
                res.push(String.fromCharCode(val) + String.fromCharCode(next));
            } else {
                res.push(String.fromCharCode(val));
                count--;
            }
        } else res.push(String.fromCharCode(val));
    }
    return res;
}
