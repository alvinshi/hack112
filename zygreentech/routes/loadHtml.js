/**
 * Created by apple on 7/14/16.
 */
'use strict';
var router = require('express').Router();

// 加载静态html
router.get('/:htmlName', function(req, res) {
    var htmlName = req.params.htmlName;
    if (htmlName.length == 0) {
        return res.sendFile('./views/index.html');
    };
    return res.render(htmlName);
});

module.exports = router;
