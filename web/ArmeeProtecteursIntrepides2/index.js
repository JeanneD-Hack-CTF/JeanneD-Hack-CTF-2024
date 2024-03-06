const express = require('express');
const path = require('path');
const { graphqlHTTP } = require('express-graphql');
const { graphql, buildSchema } = require('graphql');

// Define your GraphQL schema
const schema = buildSchema(`

  type Query {
    hello: String
    secrets: [Secret]
    getSecretById(id: ID!): Secret
  }

  type Key {
    id: ID
    value: String
  }

  type Secret {
    type: String
    strength: Int
    key: Key
    child: Secret
  }
  
`);

const keysValues = [
    {id:0, value:"RSA"},
    {id:1, value:"Point Dash"},
    {id:2, value:"Shift Index"},
    {id:3, value:"Password"}
]

const sec = {id:3, type: "Symetric Cipher", strength: 100, key: keysValues[3], child : {
  type: "Keep diving, some more iterations left", key: "No key", child: {
    type: "One more iteration", key: "No key", child: {
      type: "One last iteration", key: "No key",  child : {
        type: "Haha i swear its the very last one :)", key: "No key",  child : {
          type: "Well Done ! Perseverance is the key ! Here is the flag : Flag{Gr@phQLcept1on}"
        }
      }
    }
  }
}}

const tmp = {id:0, type: "Asymetric Cipher", strength: 100, key: keysValues[0]};
const secretsValues = [
    tmp,
    {id:1, type: "Morse", strength: 10, key: keysValues[1]},
    {id:2, type: "Cesar", strength: 30, key: keysValues[2], child: sec},
    {id:4, type: "Symetric", strength: 99, key: keysValues[3], child: tmp}
]

// Define resolver functions
const rootValue = {
  hello: () => {return 'Hello human, are you brave enough to dive into my mysteries ?';},
  secrets: () => secretsValues,
  getSecretById: ({ id }) => secretsValues.find(secret => secret.id == id),
};

const app = express();

// Setup the GraphQL endpoint using express-graphql middleware
app.use(
  '/graphql',
  graphqlHTTP({
    schema: schema,
    rootValue: rootValue,
    graphiql: false, // Enable the GraphQL interface for easy testing in the browser
  })
);

app.use('/', function(req, res) {
  res.sendFile(path.join(__dirname, '/index.html'));
})

// Start the server
const PORT = 80;
app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}/`);
});