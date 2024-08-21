from app import create_app

def main():
    # Create an instance of the Flask application
    app = create_app()

    # Run the Flask application
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
