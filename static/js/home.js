var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var _this = this;
/**
 * @author Akankshi Gupta <akankshigp12345@gmail.com>
 */
var makeRequest = function (url) { return __awaiter(_this, void 0, void 0, function () {
    var response, error_1;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                _a.trys.push([0, 3, , 4]);
                return [4 /*yield*/, fetch(url)];
            case 1:
                response = _a.sent();
                return [4 /*yield*/, response.json()];
            case 2: return [2 /*return*/, _a.sent()];
            case 3:
                error_1 = _a.sent();
                console.log("Error at makeRequest:  " + error_1.message);
                return [2 /*return*/, null];
            case 4: return [2 /*return*/];
        }
    });
}); };
var manipulate = function (id, value) {
    document.getElementById(id).innerHTML = value;
};
var updateVoteCount = function (id, upvote) {
    var vote_count_element = document.getElementById(id);
    if (upvote) {
        var increment_count = parseInt(vote_count_element.innerHTML) + 1;
        vote_count_element.innerHTML = increment_count.toString();
    }
    else {
        var increment_count = parseInt(vote_count_element.innerHTML) - 1;
        vote_count_element.innerHTML = increment_count.toString();
    }
};
var toggleIcon = function (id, icon_class_to_add, icon_class_to_remove) {
    try {
        var element = document.getElementById(id);
        element.classList.remove(icon_class_to_remove);
        element.classList.add(icon_class_to_add);
    }
    catch (error) {
        console.error('Error at ToggleIcon  : ', error.message);
    }
};
var votePost = function (post_id) { return __awaiter(_this, void 0, void 0, function () {
    var url, response, error_2;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                _a.trys.push([0, 2, , 3]);
                url = "/api/vote_post/" + post_id;
                return [4 /*yield*/, makeRequest(url)];
            case 1:
                response = _a.sent();
                if (response.message == 'Voted the post!') {
                    toggleIcon("vote-" + post_id, 'fa-check-circle', 'fa-check');
                    updateVoteCount("vote-count-" + post_id, true);
                }
                else {
                    toggleIcon("vote-" + post_id, 'fa-check', 'fa-check-circle');
                    updateVoteCount("vote-count-" + post_id, false);
                }
                return [3 /*break*/, 3];
            case 2:
                error_2 = _a.sent();
                console.log("Error making request : " + error_2.message);
                return [3 /*break*/, 3];
            case 3: return [2 /*return*/];
        }
    });
}); };
var voteAnswer = function (answer_id) { return __awaiter(_this, void 0, void 0, function () {
    var url, response, error_3;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                _a.trys.push([0, 2, , 3]);
                url = "/api/vote_answer/" + answer_id;
                return [4 /*yield*/, makeRequest(url)];
            case 1:
                response = _a.sent();
                if (response.message == 'Voted the answer!') {
                    toggleIcon("answer-" + answer_id, 'fa-check-circle', 'fa-check');
                    updateVoteCount("answer-vote-count-" + answer_id, true);
                }
                else {
                    toggleIcon("answer-" + answer_id, 'fa-check', 'fa-check-circle');
                    updateVoteCount("answer-vote-count-" + answer_id, false);
                }
                return [3 /*break*/, 3];
            case 2:
                error_3 = _a.sent();
                console.log("Error making request : " + error_3.message);
                return [3 /*break*/, 3];
            case 3: return [2 /*return*/];
        }
    });
}); };
var updateSavedButton = function (state, post_id) {
    /**if the state is true means a new post was saved */
    var element_id = "saved-" + post_id;
    var element = document.getElementById(element_id);
    if (state == true) {
        element.innerHTML = 'Save';
    }
    else if (state == false) {
        /**else if the state is false, post have been unsaved */
        element.innerHTML = 'Unsave';
    }
};
var savePost = function (post_id) { return __awaiter(_this, void 0, void 0, function () {
    var url, response, error_4;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                _a.trys.push([0, 2, , 3]);
                url = "/api/save/" + post_id;
                return [4 /*yield*/, makeRequest(url)];
            case 1:
                response = _a.sent();
                if (response.message == 'Unsaved the answer!') {
                    toggleIcon("saved-" + post_id, 'far', 'fas');
                }
                else {
                    toggleIcon("saved-" + post_id, 'fas', 'far');
                }
                return [3 /*break*/, 3];
            case 2:
                error_4 = _a.sent();
                console.warn(error_4.message);
                return [3 /*break*/, 3];
            case 3: return [2 /*return*/];
        }
    });
}); };
var reportPost = function (post_id) { return __awaiter(_this, void 0, void 0, function () {
    var url, response, error_5;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                _a.trys.push([0, 2, , 3]);
                url = "/api/report_post/" + post_id;
                return [4 /*yield*/, makeRequest(url)];
            case 1:
                response = _a.sent();
                if (response.message == 'Reported!') {
                    toggleIcon("report-post-" + post_id, 'fas', 'far');
                }
                return [3 /*break*/, 3];
            case 2:
                error_5 = _a.sent();
                console.error("Error at Report Post : " + error_5.message);
                return [3 /*break*/, 3];
            case 3: return [2 /*return*/];
        }
    });
}); };
var reportAnswer = function (answer_id) { return __awaiter(_this, void 0, void 0, function () {
    var url, response, error_6;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                _a.trys.push([0, 2, , 3]);
                url = "/api/report_answer/" + answer_id;
                return [4 /*yield*/, makeRequest(url)];
            case 1:
                response = _a.sent();
                if (response.message == 'Reported!') {
                    toggleIcon("report-answer-" + answer_id, 'fas', 'far');
                }
                return [3 /*break*/, 3];
            case 2:
                error_6 = _a.sent();
                console.error("Error at Report Answer : " + error_6.message);
                return [3 /*break*/, 3];
            case 3: return [2 /*return*/];
        }
    });
}); };
var reportAccount = function (account_id) { return __awaiter(_this, void 0, void 0, function () {
    var url, response, error_7;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                _a.trys.push([0, 2, , 3]);
                url = "/api/report_account/" + account_id;
                return [4 /*yield*/, makeRequest(url)];
            case 1:
                response = _a.sent();
                if (response.message == 'Reported!') {
                    toggleIcon("report-account-" + account_id, 'fas', 'far');
                }
                return [3 /*break*/, 3];
            case 2:
                error_7 = _a.sent();
                console.error("Error at Report Account : " + error_7.message);
                return [3 /*break*/, 3];
            case 3: return [2 /*return*/];
        }
    });
}); };
var convertDateFormat = function (date, id) {
    var date_obj = new Date(date);
    var time_string = date_obj.toDateString().toString().slice(4) + " at " + date_obj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    document.getElementById(id).innerHTML = time_string.toString();
};
var Validate = function () {
    var upload_element = document.getElementById("upload");
    for (var i = 0; i < upload_element.files.length; i++) {
        var filetype = upload_element.files.item(i).type;
        var file_size = upload_element.files.item(i).size;
        if (filetype.includes('image') || filetype.includes('video')) {
            console.log(file_size);
            if (file_size < 20000000) {
                return true;
            }
            else {
                upload_element.value = "";
                alert("File too huge!");
            }
        }
        else {
            upload_element.value = "";
            alert("Invalid Media");
        }
    }
};
var createReplyCard = function (comment, user) {
    console.log(comment.author.username == user);
    var card = "<div class=\"card h-100\">";
    if (comment.author.username === user) {
        card += "<div class=\"dropdown\">\n        <button class=\"btn dropdown-toggle\" type=\"button\" id=\"dropdownMenuButton-" + comment.reply.id + "\"\n          data-bs-toggle=\"dropdown\" aria-expanded=\"false\">\n          ...\n        </button>\n        <ul class=\"dropdown-menu\" aria-labelledby=\"dropdownMenuButton-" + comment.reply.id + "\">\n          <li><button id=\"delete-post-" + comment.reply.id + "\" data-bs-toggle=\"modal\"\n              data-bs-target=\"#delete-modal-" + comment.reply.id + "\" class=\"dropdown-item\">Delete </button></li>\n        </ul>\n      </div>\n\n      <div class=\"modal fade\" id=\"delete-modal-" + comment.reply.id + "\" tabindex=\"-1\"\n        aria-labelledby=\"modal-label-" + comment.reply.id + "\" aria-hidden=\"true\">\n        <div class=\"modal-dialog\">\n          <div class=\"modal-content\">\n            <div class=\"modal-header\">\n              <h5 class=\"modal-title\" id=\"modal-label-" + comment.reply.id + "\">Are you sure?</h5>\n              <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"modal\" aria-label=\"Close\"></button>\n            </div>\n            <div class=\"modal-body\">\n              Once the answer is deleted, can never be restored. Do you want to continue?\n            </div>\n            <div class=\"modal-footer\">\n              <button type=\"button\" class=\"btn btn-success\" data-bs-dismiss=\"modal\">No, Cancel</button>\n              <a type=\"button\" class=\"btn btn-danger\" href=\"/post/delete_answer/" + comment.reply.id + "\">Yes, Delete\n                it</a>\n            </div>\n          </div>\n        </div>\n      </div>";
    }
    card += "<div class=\"container-fluid\">\n        <div class=\"card-footer row\">\n          <div class=\"col\">\n            <small> @" + comment.author.username + " comments:</small>\n          </div>\n          <div class=\"col d-flex flex-row-reverse\">";
    if (comment.reply.already_voted) {
        card += " <i class=\"fas fa-check-circle\" id = \"answer-" + comment.reply.id + "\" title = \"Remove Support\"\n              onclick=\"voteAnswer(" + comment.reply.id + ")\"></i>";
    }
    else {
        card += "<i class=\"fas fa-check\" id = \"answer-" + comment.reply.id + "\" title = \"Support\"\n  onclick = \"voteAnswer(" + comment.reply.id + ")\" >\n    </i>\n  ";
    }
    card +=
        "&nbsp; &nbsp; &nbsp;\n    <i class=\"far fa-flag\" id = \"report-answer-" + comment.reply.id + "\" data-bs-toggle=\"modal\"\n  data-bs-target=\"#report-modal-" + comment.reply.id + "\" onclick = \"reportAnswer(" + comment.reply.id + ")\" > </i>\n      <div class= \"modal fade\" id = \"report-modal-" + comment.reply.id + "\" tabindex=\"-1\" aria-labelledby=\"modal-label-" + comment.reply.id + "\" aria-hidden=\"true\" >\n    <div class=\"modal-dialog\">\n      <div class=\"modal-content\">\n        <div class=\"modal-header\">\n          <h5 class=\"modal-title\" id=\"modal-label-" + comment.reply.id + "\"> Comment was reported!</h5>\n            <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"modal\" aria-label=\"Close\"></button>\n              </div>\n              <div class=\"modal-body\">\n                We'll check this post and if it is against our policy, we will remove it. Thank you so much\n                  </div>\n                  <div class=\"modal-footer\">\n                    <button type=\"button\" class=\"btn btn-primary\" data-bs-dismiss=\"modal\"> Okay </button>\n                      </div>\n                      </div>\n                      </div>\n                      </div>\n                        </div>\n                        </div>\n                        </div>\n                          ";
    var date_obj = new Date(comment.reply.posted_on);
    card += "<div class=\"card-body\">\n        <p class=\"card-text\"> " + comment.reply.text + " </a></p>\n        <small class=\"text-secondary\"> On\n          <time datetime=\"" + comment.reply.posted_on + "|date:'c'}\"\n            id=\"time-" + comment.reply.id + "\">" + (date_obj.toDateString().toString().slice(4) + " at " + date_obj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })) + "</time>\n        </small>\n        &nbsp; &nbsp; &nbsp;\n      </div>";
    return card;
};
var setPageNumber = function (answer_id, page_number, user) {
    var button = document.getElementById("load-replies-button-" + answer_id);
    button.setAttribute('onClick', "fetchComment(" + answer_id + "," + page_number + ",'" + user + "')");
};
var fetchComment = function (answer_id, page_number, user) { return __awaiter(_this, void 0, void 0, function () {
    var response, data, parent_element, load_button, _i, data_1, comment;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: return [4 /*yield*/, makeRequest("/api/fetch_answer_replies/" + answer_id + "/" + page_number)];
            case 1:
                response = _a.sent();
                data = response.data;
                parent_element = document.getElementById("load-replies-" + answer_id);
                if (Object.keys(data).length === 0) {
                    load_button = document.getElementById("load-replies-button-" + answer_id);
                    load_button.remove();
                }
                else {
                    for (_i = 0, data_1 = data; _i < data_1.length; _i++) {
                        comment = data_1[_i];
                        console.log(comment);
                        parent_element.insertAdjacentHTML('afterbegin', createReplyCard(comment, user));
                    }
                }
                setPageNumber(answer_id, page_number + 1, user);
                return [2 /*return*/];
        }
    });
}); };
document.addEventListener('DOMContentLoaded', function () {
    var elements = document.querySelectorAll('time');
    elements.forEach(function (element) {
        var iso_time = element.getAttribute("datetime");
        var id = element.getAttribute('id');
        convertDateFormat(iso_time, id);
    });
});
