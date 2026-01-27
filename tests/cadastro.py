from playwright.sync_api import sync_playwright
import numpy as np
from services.user_service import UserService

total_testes = 0
testes_validos = 0

def correct_cadastro():
    with sync_playwright() as p:
        
        global total_testes, testes_validos
        total_testes += 1
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Teste de fluxo de cadastro
        page.goto("http://localhost:5000")
        page.locator('a[href="/cadastro"]').click()
        page.locator('[name="nome"]').fill("Pedro")
        email = f"pedro{np.random.randint(1000)}@outlook.com"
        page.locator('[name="email"]').fill(email)
        page.locator('[name="password"]').fill("pedro0206")
        page.locator('button[type="submit"]').click()
        try:
            assert page.url == "http://localhost:5000/login"
            testes_validos += 1
            print("✅ Teste de cadastro válido passou.")
        except AssertionError:
            print("❌ Teste de cadastro válido falhou.")
        
        UserService.delete_user(email)

        context.close()
        browser.close()


def cadastro_test():
    correct_cadastro()

if __name__ == "__main__":
    cadastro_test()
    print(f"{testes_validos} de {total_testes} testes passaram.")