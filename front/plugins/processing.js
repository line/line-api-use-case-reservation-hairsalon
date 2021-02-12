/**
 * 処理中画面表示プラグイン
 *
 * @return {Object} 
 */
const VueProcessing = () => {
    const _id = "_id_loading_component";
    const _default = 0;
    const _svg = "PCEtLSBCeSBTYW0gSGVyYmVydCAoQHNoZXJiKSwgZm9yIGV2ZXJ5b25lLiBNb3JlIEAgaHR0cDovL2dvby5nbC83QUp6YkwgLS0+DQo8c3ZnIHdpZHRoPSI0NCIgaGVpZ2h0PSI0NCIgdmlld0JveD0iMCAwIDQ0IDQ0IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0cm9rZT0iI2ZmZiI+DQogICAgPGcgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIiBzdHJva2Utd2lkdGg9IjIiPg0KICAgICAgICA8Y2lyY2xlIGN4PSIyMiIgY3k9IjIyIiByPSIxIj4NCiAgICAgICAgICAgIDxhbmltYXRlIGF0dHJpYnV0ZU5hbWU9InIiDQogICAgICAgICAgICAgICAgYmVnaW49IjBzIiBkdXI9IjEuOHMiDQogICAgICAgICAgICAgICAgdmFsdWVzPSIxOyAyMCINCiAgICAgICAgICAgICAgICBjYWxjTW9kZT0ic3BsaW5lIg0KICAgICAgICAgICAgICAgIGtleVRpbWVzPSIwOyAxIg0KICAgICAgICAgICAgICAgIGtleVNwbGluZXM9IjAuMTY1LCAwLjg0LCAwLjQ0LCAxIg0KICAgICAgICAgICAgICAgIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiAvPg0KICAgICAgICAgICAgPGFuaW1hdGUgYXR0cmlidXRlTmFtZT0ic3Ryb2tlLW9wYWNpdHkiDQogICAgICAgICAgICAgICAgYmVnaW49IjBzIiBkdXI9IjEuOHMiDQogICAgICAgICAgICAgICAgdmFsdWVzPSIxOyAwIg0KICAgICAgICAgICAgICAgIGNhbGNNb2RlPSJzcGxpbmUiDQogICAgICAgICAgICAgICAga2V5VGltZXM9IjA7IDEiDQogICAgICAgICAgICAgICAga2V5U3BsaW5lcz0iMC4zLCAwLjYxLCAwLjM1NSwgMSINCiAgICAgICAgICAgICAgICByZXBlYXRDb3VudD0iaW5kZWZpbml0ZSIgLz4NCiAgICAgICAgPC9jaXJjbGU+DQogICAgICAgIDxjaXJjbGUgY3g9IjIyIiBjeT0iMjIiIHI9IjEiPg0KICAgICAgICAgICAgPGFuaW1hdGUgYXR0cmlidXRlTmFtZT0iciINCiAgICAgICAgICAgICAgICBiZWdpbj0iLTAuOXMiIGR1cj0iMS44cyINCiAgICAgICAgICAgICAgICB2YWx1ZXM9IjE7IDIwIg0KICAgICAgICAgICAgICAgIGNhbGNNb2RlPSJzcGxpbmUiDQogICAgICAgICAgICAgICAga2V5VGltZXM9IjA7IDEiDQogICAgICAgICAgICAgICAga2V5U3BsaW5lcz0iMC4xNjUsIDAuODQsIDAuNDQsIDEiDQogICAgICAgICAgICAgICAgcmVwZWF0Q291bnQ9ImluZGVmaW5pdGUiIC8+DQogICAgICAgICAgICA8YW5pbWF0ZSBhdHRyaWJ1dGVOYW1lPSJzdHJva2Utb3BhY2l0eSINCiAgICAgICAgICAgICAgICBiZWdpbj0iLTAuOXMiIGR1cj0iMS44cyINCiAgICAgICAgICAgICAgICB2YWx1ZXM9IjE7IDAiDQogICAgICAgICAgICAgICAgY2FsY01vZGU9InNwbGluZSINCiAgICAgICAgICAgICAgICBrZXlUaW1lcz0iMDsgMSINCiAgICAgICAgICAgICAgICBrZXlTcGxpbmVzPSIwLjMsIDAuNjEsIDAuMzU1LCAxIg0KICAgICAgICAgICAgICAgIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiAvPg0KICAgICAgICA8L2NpcmNsZT4NCiAgICA8L2c+DQo8L3N2Zz4=";

    const _loadingHtml = (type, message) => {
        let div = "";
        message = (typeof(message)=="undefined") ? "" : message;

        switch (type) {
        case 0:
            div = `
                <div id='${_id}' class='loader-wrap'>
                    <div class="loader">
                        <div class="inner one"></div>
                        <div class="inner two"></div>
                        <div class="inner three"></div>
                    </div>
                    <div class="loader-message"'>${message}</div>
                </div>`;
                break;
        case 1:
            div = `
                <div id='${_id}' class='loader-wrap'>
                    <div class='loader-image' style='position:absolute; margin:auto; left:0; top:0; right:0; bottom:0; width:80px; height:80px;'>
                        <img src='data:image/svg+xml;base64,${_svg}' style='width:80px; height=auto;' alt='${message}' />
                    </div>
                    <div class="loader-message"'>${message}</div>
                </div>`;
            break;
        }
    
        return div;
    }

    
    return {
        show(type, message) {
            type = (typeof(type)=="undefined") ? _default : type;
            let div = _loadingHtml(type, message);
            let element = document.createElement("div");
            element.innerHTML = div;
            document.body.appendChild(element);
            let elements = document.getElementsByClassName("loader-wrap");
            for (let element of elements) {
                element.style.display = "block";
            }
        },
        hide() {
            try { document.getElementById(_id).remove(); } catch (ex) {}
        }
    }
}

export default ({}, inject) => {
    inject("processing", VueProcessing());
}
