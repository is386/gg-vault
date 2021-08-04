let search_url = "http://127.0.0.1:8080/search"

function search() {
    let urlParams = new URLSearchParams(window.location.search);
    let searchTerm = urlParams.get("searchTerm");

    $.ajax({
        url: search_url,
        type: "POST",
        dataType: "json",
        data: {"query": searchTerm},
        headers: {"Authorization": "Bearer " + localStorage.ggToken},
        complete: function(data) {
            let status = data.status;
            if (status != 200) {
                return;
            }
            populateResults(data.responseJSON);
        }
    });
}

function populateResults(games) {
    let container = $("#results");
    for (let g of games) {
        if (!g.cover) {
            continue;
        }
        let card = $(`
        <div class="col-auto mb-3">
            <div id=${g.id} class="card" style="width: 18rem;">
                <img src="${g.cover.url}" class="card-img-top">
                <div class="card-body">
                    <h5 class="card-title">${g.name}</h5>
                </div>
            </div>
        </div>`)
        container.append(card);
    }

}