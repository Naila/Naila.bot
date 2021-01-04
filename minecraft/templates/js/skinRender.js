const nameInput = document.getElementById("player_name");
const capeInput = document.getElementById("cape")

nameInput.addEventListener("keyup", debounce(updateScene, 500))
capeInput.addEventListener("keyup", debounce(updateScene, 500))

const skinRender = new SkinRender({
    controls: {
        zoom: false,
        pan: false
    },
    canvas: {
        width: 200,
        height: 400
    }
}, document.getElementById("player_model"))

skinRender.render({
    username: "_Kanin",
    cape: "minecraft"
})

function getCapes() {
    const name = $("#player_name").val()
    const capes = []
    if (name && name.length > 0) {
        fetch(`https://api.capes.dev/load/${name}`)
            .then(response => {
                if (response.status !== 200) {
                    console.log("Status code: " + response.status)
                } else {
                    response.json().then(data => {
                        Object.keys(data).forEach(item => {
                            if (data[item]["exists"] === true) {
                                capes.push(item)
                            }
                        })
                    })
                }
            })
    }
    return capes
}

function updateScene() {
    skinRender.clearScene()
    const name = $("#player_name").val()
    const cape = $("#cape").val()
    const options = {}
    if (name.match("https?:\\/\\/(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b([-a-zA-Z0-9()@:%_\\+.~#?&//=]*)")) {
        options.url = name
    } else {
        options.username = name
    }
    if (cape && cape.length > 0) {
        if (cape.includes("capes.dev") || !cape.startsWith("http")) {
            options.cape = cape
        } else {
            options.capeUrl = cape
        }
    }
    skinRender.render(options)
}

function debounce(callback, delay) {
    let timeout
    return function () {
        clearTimeout(timeout)
        timeout = setTimeout(callback, delay)
    }
}