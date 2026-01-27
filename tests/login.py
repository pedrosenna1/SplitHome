from playwright.sync_api import sync_playwright


dados = {
    'email': 'pedro@example.com',
    'password': 'pedro0206',
}

testes_validos = 0
total_testes = 0

def login_test():
    with sync_playwright() as p:
        
        global total_testes, testes_validos
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

if __name__ == "__main__":
    login_test()
    print(f"\nTestes válidos: {testes_validos}/{total_testes}")
