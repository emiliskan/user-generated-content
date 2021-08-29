const dbName = "ugc_db";
const conn = new Mongo();
const db = conn.getDB(dbName);

const collectionSettings = [
    {
        name: "movies"
    },
    {
        name: "user_bookmarks",
        shardKey: "_id"
    },
    {
        name: "movie_scores",
        shardKey: "movie_id",
        indexFields: ["movie_id", "score"]
    },
    {
        name: "reviews",
        shardKey: "movie_id",
        indexFields: [
            "movie_id",
            "pub_date",
            "movie_rating_score",
        ]
    },
    {
        name: "review_scores",
        shardKey: "review_id",
        indexFields: ["score"]
    },
];

sh.enableSharding(dbName);

collectionSettings.forEach((collection) => {
    const collectionName = collection.name;
    const shardKey = collection.shardKey;
    const indexFields = collection.indexFields;

    db.createCollection(collectionName);
    if (shardKey !== undefined) {
        sh.shardCollection(`${dbName}.${collectionName}`, {[shardKey]: "hashed"});
    }
    if (indexFields !== undefined) {
        indexFields.forEach((field) => {
            db[collectionName].createIndex({[field]: -1});
        })
    }
});