let search_url = "api/search"
let add_url = "api/add"
let games_url = "api/games"
let games;
let ids = [];
let added = [];
let total;
let resultsIndex = 0;

// Sends a request to search for games
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
                $("#no-results").attr({"hidden": false});
                return;
            }
            $("#no-results").attr({"hidden": true});
            checkGames(data.responseJSON);
        }
    });
}

// Sends a request to get the games the user already owns
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
            } else {
                populateResults(searchGames, null);
            }
        }
    });
}

// Populates the search results
function populateResults(searchGames, myGames) {
    if (myGames) {
        for (let g of myGames.wishlist.concat(myGames.my_games)) {
            ids.push(g.id)
        }
    }
    games = searchGames;
    total = games.length;
    let end = resultsIndex + 8;
    loadGames(resultsIndex, end);
}

// Loads the number of games in the search results within a range
function loadGames(start, end) {
    let i = start;
    let container = $("#results");
    container.empty();

    while (i < end && i < games.length) {
        let g = games[i];

        if (ids.includes(g.id) || !g.cover) {
            i++;
            end++;
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
        let footer = $("<div class=\"card-footer\">Added</div>")

        if (!added.includes(g.id)) {
            let myGamesBtn = $("<button id=\"my-games-btn\" class=\"btn btn-success mt-2\"><i class=\"fa fa-plus\"></i> My Games</button>");
            let wishBtn = $("<button id=\"wish-btn\" class=\"btn btn-primary mt-2\"><i class=\"fa fa-plus\"></i> Wishlist</button>");
            
            myGamesBtn.click(function() {
                addGame(g.id, 0);
            });
    
            wishBtn.click(function() {
                addGame(g.id, 1);
            });
            card.find(".card-body").append(myGamesBtn).append(wishBtn);
        } else {
            card.find("#" + g.id).addClass( "disabled");
            card.find("#" + g.id).append(footer);
        }

        container.append(card);
        i++;
    }
}

// Sends a request to add a game to a user's lists
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
    added.push(gameId);
    let card = $("#" + gameId);
    card.addClass( "disabled");
    card.find("#my-games-btn").remove();
    card.find("#wish-btn").remove();
    let footer = $("<div class=\"card-footer\">Added</div>")
    card.append(footer);
}

// Advances the results screen by 8 entries
function next() {
    resultsIndex += 9;
    if (resultsIndex > games.length) {
        resultsIndex -= 9;
    }
    let end = resultsIndex + 8;
    loadGames(resultsIndex, end);
}

// Goes backward by 8 entries
function back() {
    resultsIndex -= 9;
    if (resultsIndex < 0) {
        resultsIndex = 0;
    }
    let end = resultsIndex + 8;
    loadGames(resultsIndex, end);
}