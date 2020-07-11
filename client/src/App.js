import React from 'react';
import TopBar from './components/TopBar.js';
import Welcome from './components/Welcome.js';

import { ApolloProvider } from '@apollo/react-hooks';
import ApolloClient from 'apollo-boost';

const client = new ApolloClient({
  uri: 'http://127.0.0.1:5000/graphqltesting',
});


const App = () => {
  return (
    <ApolloProvider client={client}>
        <div>
          <TopBar />
          <Welcome />
      </div>
    </ApolloProvider>
  )
};

export default App;
