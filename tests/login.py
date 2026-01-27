from playwright.sync_api import sync_playwright


dados = {
    'email': 'pedro@example.com',
    'password': 'pedro0206',
}

testes_validos = 0
total_testes = 0

def correct_login():
    with sync_playwright() as p:
        
        global total_testes, testes_validos,dados
        total_testes += 1
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Teste de fluxo de login
        page.goto("http://localhost:5000/login")
        page.locator('[name="email"]').fill(dados['email'])
        page.locator('[name="password"]').fill(dados['password'])
        page.locator('button[type="submit"]').click()

        try:
            assert page.url == "http://localhost:5000/home"
            print("✅ Teste de login bem-sucedido.")
            testes_validos += 1
        
        except AssertionError:
            print("❌ Teste de login falhou.")

        context.close()
        browser.close()

def email_incorrect():
    with sync_playwright() as p:
        
        global total_testes, testes_validos,dados
        total_testes += 1
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Teste de fluxo de login incorreto
        page.goto("http://localhost:5000/login")
        page.locator('[name="email"]').fill("pedro@gmail.com")
        page.locator('[name="password"]').fill(dados['password'])
        page.locator('button[type="submit"]').click()
        
        try:
            assert page.locator('[class="error-message"]').inner_text() == "Credenciais inválidas"
            testes_validos += 1
            print("✅ Teste de login com email incorreto bem-sucedido.")
        except AssertionError:
            print("❌ Teste de login com email incorreto falhou.")
        
        context.close()
        browser.close()

def password_incorrect():
    with sync_playwright() as p:
        
        global total_testes, testes_validos,dados
        total_testes += 1
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Teste de fluxo de login incorreto
        page.goto("http://localhost:5000/login")
        page.locator('[name="email"]').fill(dados['email'])
        page.locator('[name="password"]').fill("wrongpassword")
        page.locator('button[type="submit"]').click()
        
        try:
            assert page.locator('[class="error-message"]').inner_text() == "Credenciais inválidas"
            testes_validos += 1
            print("✅ Teste de login com senha incorreta bem-sucedido.")
        except AssertionError:
            print("❌ Teste de login com senha incorreta falhou.")
        
        context.close()
        browser.close()
            

def login_test():
    correct_login()
    email_incorrect()
    password_incorrect()

if __name__ == "__main__":
    login_test()
    print(f"\nTestes válidos: {testes_validos}/{total_testes}")
