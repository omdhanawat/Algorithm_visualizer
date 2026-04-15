import { Component, type ErrorInfo, type ReactNode } from 'react';

interface Props {
  children?: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="p-6 m-4 text-red-100 bg-red-900/40 border border-red-500/50 rounded-xl backdrop-blur-md shadow-2xl">
          <h2 className="text-xl font-bold mb-3 flex items-center gap-2 italic">
            <span className="text-red-400">⚠️</span> Visualizer Rendering Error
          </h2>
          <p className="text-sm text-slate-300 font-mono mb-4 bg-black/40 p-3 rounded border border-white/10 overflow-auto max-h-[150px]">
            {this.state.error?.message}
          </p>
          <button 
            onClick={() => this.setState({ hasError: false })}
            className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-all text-sm font-semibold shadow-lg shadow-red-500/20"
          >
            Try Refreshing Component
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
