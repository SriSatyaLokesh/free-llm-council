import React from 'react';

/**
 * ErrorBoundary to catch unexpected runtime render errors
 * and prevent complete blank screens.
 */
export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Unhandled render error caught by ErrorBoundary:', error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
    if (this.props.onReset) {
      this.props.onReset();
    }
  };

  render() {
    if (this.state.hasError) {
      return (
        <div
          style={{
            padding: '24px',
            margin: '16px',
            background: 'var(--surface-raised, #1e293b)',
            border: '1px solid var(--border, #334155)',
            borderRadius: '8px',
            color: 'var(--fg, #f8fafc)',
            textAlign: 'center',
          }}
          role="alert"
        >
          <h3 style={{ margin: '0 0 8px 0', fontSize: '1rem', color: 'var(--destructive, #ef4444)' }}>
            Something went wrong displaying this section
          </h3>
          <p style={{ margin: '0 0 16px 0', fontSize: '0.85rem', color: 'var(--fg-muted, #94a3b8)' }}>
            {this.state.error?.message || 'An unexpected rendering error occurred.'}
          </p>
          <button
            type="button"
            onClick={this.handleReset}
            style={{
              padding: '6px 14px',
              fontSize: '0.8rem',
              fontWeight: 600,
              background: 'var(--accent, #3b82f6)',
              color: '#ffffff',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            Try Again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
