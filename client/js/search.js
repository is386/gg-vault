let search_url = "http://127.0.0.1:8080/search"
let add_url = "http://127.0.0.1:8080/add"
let games_url = "http://127.0.0.1:8080/games"

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
            checkGames(data.responseJSON);
        }
    });
}

function checkGames(searchGames) {
    $.ajax({
        url: games_url,
        type: "POST",
        dataType: "json",
        headers: {"Authorization": "Bearer " + localStorage.ggToken},
        complete: function(data) {
            let status = data.status;
            if (status == 200) {
                populateResults(searchGames, data.responseJSON);
            }
        }
    });
}

function populateResults(searchGames, myGames) {
    let ids = [];
    for (let g of myGames.wishlist.concat(myGames.my_games)) {
        ids.push(g.id)
    }
    console.log(ids);
    let container = $("#results");
    for (let g of searchGames) {
        if (ids.includes(g.id) || !g.cover) {
            continue;
        }
        let card = $(`
        <div class="col-auto mb-3">
            <div id=${g.id} class="card text-center" style="width: 18rem;">
                <img src="${g.cover.url}" class="card-img-top">
                <div class="card-body">
                    <h5 class="card-title">${g.name}</h5>
                </div>
            </div>
        </div>`)
        let myGamesBtn = $("<button class=\"btn btn-success mt-2\"><i class=\"fa fa-plus\"></i> My Games</button>");
        let wishBtn = $("<button class=\"btn btn-primary mt-2\"><i class=\"fa fa-plus\"></i> Wishlist</button>");
        myGamesBtn.click(function() {
            addGame(g.id, 0);
        });
        wishBtn.click(function() {
            addGame(g.id, 1);
        });
        card.find(".card-body").append(myGamesBtn).append(wishBtn);
        container.append(card);
    }
}

function addGame(gameId, wishlist) {
    if (wishlist) {
        formData = {"game_id": gameId, "wishlist": 1};
    } else {
        formData = {"game_id": gameId};
    }
    $.ajax({
        url: add_url,
        type: "POST",
        dataType: "json",
        data: formData,
        headers: {"Authorization": "Bearer " + localStorage.ggToken},
        complete: function(data) {
        }
    });
}