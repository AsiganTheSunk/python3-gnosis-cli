REMOVE_OLD_CONTRACTS = rm -rf ./safe/safe-contracts-development/build/
COMPILE = truffle compile
TEST = truffle test
MIGRATE = truffle migrate
MIGRATE_RESET = --reset
NPM_START = npm start
NPM_INSTALL = npm install
GANACHE_LAUNCH = ganache-cli -d

launch_ganache:
	$(GANACHE_LAUNCH)

compile:
	$(COMPILE)

test_contracts:
	$(TEST)

soft_migrate:
	$(MIGRATE)

hard_migrate:
	$(MIGRATE) $(MIGRATE_RESET)

launch_client:
	$(NPM_START) $(APP_CLIENT)

install:
	$(NPM_INSTALL)

all:
	make compile
	make hard_migrate
	make test_contracts


