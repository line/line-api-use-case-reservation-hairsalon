/**
 * F5、右クリック無効化プラグイン
 *
 * @param {Object} store
 */
export default ({store}) => {
    if (process.env.NODE_ENV != "production") { return; }
    let ctlKey = false;
    window.document.addEventListener("keydown", (e)=>{
        if (e.ctrlKey) ctlKey = true;
        if ((e.which || e.keyCode) == 82 && ctlKey) e.preventDefault();
        if ((e.which || e.keyCode) == 116) e.preventDefault();
    }, false);
    window.document.addEventListener("keyup", (e)=>{
        if (e.ctrlKey) ctlKey = false;
    }, false);
    window.document.addEventListener("contextmenu", (e)=>{
        e.preventDefault();
    }, false);
}
