import './App.css'
import { StytchLogin, useStytchUser, useStytch, Products } from "@stytch/react";

function App() {
  const { user } = useStytchUser();
  const stytch = useStytch();

  const config = {
    products: [Products.passwords],
    passwordOptions: {
      loginRedirectURL: "http://localhost:5173/",
      resetPasswordRedirectURL: "http://localhost:5173/reset"
    },
    sessionOptions: {
      sessionDurationMinutes: 1440
    }
  };

  const token = stytch.session.getTokens()?.session_token;

  return (
    <div>
      {!user ? (
        <StytchLogin config={config} />
      ) : (
        <div>
          <p>Bienvenido {user.emails[0].email}!</p>
          <p>Tu token para Cline:</p>
          <textarea 
            readOnly 
            value={token || ''} 
            style={{width: '100%', height: '100px'}}
          />
          <button onClick={() => navigator.clipboard.writeText(token)}>
            Copiar token
          </button>
        </div>
      )}
    </div>
  );
}

export default App;