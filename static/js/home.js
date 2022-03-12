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
    if (upvote) {
        var vote_count_element = document.getElementById(id);
        var increment_count = parseInt(vote_count_element.innerHTML) + 1;
        vote_count_element.innerHTML = increment_count.toString();
    }
    else {
        var vote_count_element = document.getElementById(id);
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
                    manipulate("vote-" + answer_id, 'Un-Vote');
                    updateVoteCount("vote-count-" + answer_id, true);
                }
                else {
                    manipulate("vote-" + answer_id, 'Vote');
                    updateVoteCount("vote-count-" + answer_id, false);
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
var reportAccount = function (account_id) { return __awaiter(_this, void 0, void 0, function () {
    var url, response, error_6;
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
                error_6 = _a.sent();
                console.error("Error at Report Account : " + error_6.message);
                return [3 /*break*/, 3];
            case 3: return [2 /*return*/];
        }
    });
}); };
