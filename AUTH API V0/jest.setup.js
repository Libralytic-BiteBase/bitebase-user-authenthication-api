process.env.NODE_ENV = 'test';
process.env.TEST_PORT = 3001;

jest.setTimeout(30000); // Increase timeout to 30 seconds

afterAll(async () => {
  await new Promise(resolve => setTimeout(resolve, 500)); // Add small delay to allow connections to close
});