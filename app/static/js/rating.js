const labels = document.getElementsByClassName('rating');


for(let label of labels) {
    label.addEventListener('click', () => {
        let checked = [];

        for(let i = 0; i < labels.length; i++) {
            if (labels[i] == label) {
                checked.push(labels[i]);
                break;
            } else {
                checked.push(labels[i]);
            }
        }

        for (let item of checked) {
            if (label.getAttribute('clicked') == null) {
                item.setAttribute('clicked', '')
                document.getElementById(item.getAttribute('for')).setAttribute('checked', '');
                item.style.backgroundImage = "url('../static/images/star_checked.png')";
            } 
        }
        for(let h = checked.length; h < labels.length; h++) {
            labels[h].removeAttribute('clicked');
            document.getElementById(labels[h].getAttribute('for')).removeAttribute('checked');
            labels[h].style.backgroundImage = "url('../static/images/star.png')";
        }
    });
}