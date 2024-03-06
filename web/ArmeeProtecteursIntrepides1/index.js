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
    """
    Well done ! GraphQL Introspection can give you a lot of informations about how the API works.
    Flag : {FLAG}
  """
    id: ID
    value: String
  }

  type Secret {
    type: String
    strength: Int
    key: Key
  }
  
`);

const keysValues = [
    {id:0, value:"RSA"},
    {id:1, value:"Point Dash"},
    {id:2, value:"Shift Index"}
]

const secretsValues = [
    {id:0, type: "Asymetric Cipher", strength: 100, key: keysValues[0]},
    {id:1, type: "Morse", strength: 10, key: keysValues[1]},
    {id:2, type: "Cesar", strength: 30, key: keysValues[2]}
]

// Define resolver functions
const rootValue = {
  hello: () => {return 'Hello human! Remember, meditation and introspection are keys to Nirvana.';},
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
    graphiql: false, // Enable the GraphiQL interface for easy testing in the browser
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