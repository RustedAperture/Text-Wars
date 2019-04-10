function launchTW() {
    let i = 11;
    var x = setInterval(function() {
        i -= 1;
        console.log(i);
        if (i == 0) clearInterval(x);
    }, 1000);
}
