
function htmlContentSize(element) {
    var styles = getComputedStyle(element);

    let width = element.clientWidth - parseFloat(styles.paddingLeft) - parseFloat(styles.paddingRight);
    let height = element.clientHeight - parseFloat(styles.paddingBottom) - parseFloat(styles.paddingTop);

    return {width, height};
}

function randomNum(min, max){
    return (max-min)*Math.random() + min;
}