// @trace TASK-039
import { useState } from 'react';

interface AuthFormsProps {
  onLoginSuccess: (token: string) => void;
}

export function AuthForms({ onLoginSuccess }: AuthFormsProps) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    setLoading(true);

    const endpoint = isLogin ? '/auth/login' : '/auth/register';
    const payload = isLogin 
      ? { username, password } 
      : { username, email, password };

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Authentication failed');
      }

      if (isLogin) {
        onLoginSuccess(data.access_token);
      } else {
        setMessage('Registration successful! You can now log in.');
        setIsLogin(true);
      }
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-fantasy-card rounded-lg shadow-2xl border border-fantasy-accent/30 overflow-hidden">
        <div className="flex border-b border-fantasy-accent/20">
          <button
            type="button"
            className={`flex-1 py-4 text-center font-bold uppercase tracking-wider transition-colors
              ${isLogin 
                ? 'bg-fantasy-dark/50 text-fantasy-accent border-b-2 border-fantasy-accent' 
                : 'text-fantasy-text/60 hover:text-fantasy-accent/80 hover:bg-fantasy-dark/30'}`}
            onClick={() => { setIsLogin(true); setError(null); setMessage(null); }}
          >
            Login
          </button>
          <button
            type="button"
            className={`flex-1 py-4 text-center font-bold uppercase tracking-wider transition-colors
              ${!isLogin 
                ? 'bg-fantasy-dark/50 text-fantasy-accent border-b-2 border-fantasy-accent' 
                : 'text-fantasy-text/60 hover:text-fantasy-accent/80 hover:bg-fantasy-dark/30'}`}
            onClick={() => { setIsLogin(false); setError(null); setMessage(null); }}
          >
            Register
          </button>
        </div>

        <div className="p-8">
          <h2 className="text-2xl font-bold text-center text-fantasy-text mb-6 drop-shadow-sm">
            {isLogin ? 'Enter the Realm' : 'Join the Adventure'}
          </h2>

          {error && (
            <div className="mb-6 p-3 bg-fantasy-danger/20 border border-fantasy-danger text-fantasy-danger rounded text-sm text-center">
              {error}
            </div>
          )}

          {message && (
            <div className="mb-6 p-3 bg-fantasy-success/20 border border-fantasy-success text-fantasy-success rounded text-sm text-center">
              {message}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-fantasy-text/80 mb-1">Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="w-full bg-fantasy-dark border border-fantasy-accent/30 rounded p-2.5 text-fantasy-text focus:ring-1 focus:ring-fantasy-accent focus:border-fantasy-accent outline-none transition-shadow"
                placeholder="Your heroic name"
              />
            </div>

            {!isLogin && (
              <div>
                <label className="block text-sm font-medium text-fantasy-text/80 mb-1">Email</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full bg-fantasy-dark border border-fantasy-accent/30 rounded p-2.5 text-fantasy-text focus:ring-1 focus:ring-fantasy-accent focus:border-fantasy-accent outline-none transition-shadow"
                  placeholder="scrolls@domain.com"
                />
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-fantasy-text/80 mb-1">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full bg-fantasy-dark border border-fantasy-accent/30 rounded p-2.5 text-fantasy-text focus:ring-1 focus:ring-fantasy-accent focus:border-fantasy-accent outline-none transition-shadow"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-6 bg-fantasy-accent text-fantasy-dark font-bold uppercase tracking-wide py-3 px-4 rounded shadow hover:bg-yellow-500 hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Casting...' : (isLogin ? 'Login' : 'Register')}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}