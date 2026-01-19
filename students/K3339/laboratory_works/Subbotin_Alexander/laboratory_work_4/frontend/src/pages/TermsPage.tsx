import { Link } from 'react-router-dom';

export function TermsPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-md p-8">
        <h1 className="text-3xl font-bold text-center mb-2">TERMS AND CONDITIONS</h1>
        <p className="text-gray-500 text-center mb-8">
          <strong>Last updated:</strong> December 02, 2025
        </p>

        <section className="mb-8">
          <h2 className="text-xl font-bold mb-4">AGREEMENT TO OUR LEGAL TERMS</h2>
          <p className="text-gray-600 mb-4">
            We are <strong>Hokkaido Tours</strong> ("<strong>Company</strong>," "<strong>we</strong>," "<strong>us</strong>," "<strong>our</strong>"), 
            a company registered in Russia at Lomonosova 9, Saint-Petersburg, Leningradskaya oblast' 192007.
          </p>
          <p className="text-gray-600 mb-4">
            We operate the website{' '}
            <a href="http://www.hokkaido-tours.ru" className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
              http://www.hokkaido-tours.ru
            </a>{' '}
            (the "<strong>Site</strong>"), as well as any other related products and services that refer or link to these legal terms 
            (the "<strong>Legal Terms</strong>") (collectively, the "<strong>Services</strong>").
          </p>
          <p className="text-gray-600 mb-4">
            You can contact us by phone at <strong>89006662505</strong>, email at{' '}
            <a href="mailto:zzisst@mail.ru" className="text-blue-600 hover:underline">zzisst@mail.ru</a>, 
            or by mail to Lomonosova 9, Saint-Petersburg, Leningradskaya oblast' 192007, Russia.
          </p>
          <p className="text-gray-600 mb-4">
            These Legal Terms constitute a legally binding agreement made between you, whether personally or on behalf of an entity 
            ("<strong>you</strong>"), and Hokkaido Tours, concerning your access to and use of the Services. You agree that by accessing 
            the Services, you have read, understood, and agreed to be bound by all of these Legal Terms. 
            <strong> IF YOU DO NOT AGREE WITH ALL OF THESE LEGAL TERMS, THEN YOU ARE EXPRESSLY PROHIBITED FROM USING THE SERVICES 
            AND YOU MUST DISCONTINUE USE IMMEDIATELY.</strong>
          </p>
          <p className="text-gray-600 mb-4">
            The Services are intended for users who are at least 13 years of age. All users who are minors in the jurisdiction in which 
            they reside (generally under the age of 18) must have the permission of, and be directly supervised by, their parent or guardian 
            to use the Services.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-xl font-bold mb-4">TABLE OF CONTENTS</h2>
          <ol className="list-decimal list-inside text-blue-600 space-y-1">
            <li><a href="#services" className="hover:underline">OUR SERVICES</a></li>
            <li><a href="#ip" className="hover:underline">INTELLECTUAL PROPERTY RIGHTS</a></li>
            <li><a href="#userreps" className="hover:underline">USER REPRESENTATIONS</a></li>
            <li><a href="#userreg" className="hover:underline">USER REGISTRATION</a></li>
            <li><a href="#purchases" className="hover:underline">PURCHASES AND PAYMENT</a></li>
            <li><a href="#prohibited" className="hover:underline">PROHIBITED ACTIVITIES</a></li>
            <li><a href="#ugc" className="hover:underline">USER GENERATED CONTRIBUTIONS</a></li>
            <li><a href="#license" className="hover:underline">CONTRIBUTION LICENSE</a></li>
            <li><a href="#sitemanage" className="hover:underline">SERVICES MANAGEMENT</a></li>
            <li><a href="#terms" className="hover:underline">TERM AND TERMINATION</a></li>
            <li><a href="#modifications" className="hover:underline">MODIFICATIONS AND INTERRUPTIONS</a></li>
            <li><a href="#law" className="hover:underline">GOVERNING LAW</a></li>
            <li><a href="#disputes" className="hover:underline">DISPUTE RESOLUTION</a></li>
            <li><a href="#corrections" className="hover:underline">CORRECTIONS</a></li>
            <li><a href="#disclaimer" className="hover:underline">DISCLAIMER</a></li>
            <li><a href="#liability" className="hover:underline">LIMITATIONS OF LIABILITY</a></li>
            <li><a href="#indemnification" className="hover:underline">INDEMNIFICATION</a></li>
            <li><a href="#userdata" className="hover:underline">USER DATA</a></li>
            <li><a href="#electronic" className="hover:underline">ELECTRONIC COMMUNICATIONS, TRANSACTIONS, AND SIGNATURES</a></li>
            <li><a href="#misc" className="hover:underline">MISCELLANEOUS</a></li>
            <li><a href="#contact" className="hover:underline">CONTACT US</a></li>
          </ol>
        </section>

        <section id="services" className="mb-8">
          <h2 className="text-xl font-bold mb-4">1. OUR SERVICES</h2>
          <p className="text-gray-600">
            The information provided when using the Services is not intended for distribution to or use by any person or entity 
            in any jurisdiction or city where such distribution or use would be contrary to law or regulation or which would subject 
            us to any registration requirement within such jurisdiction or city. Accordingly, those persons who choose to access the 
            Services from other locations do so on their own initiative and are solely responsible for compliance with local laws, 
            if and to the extent local laws are applicable.
          </p>
        </section>

        <section id="ip" className="mb-8">
          <h2 className="text-xl font-bold mb-4">2. INTELLECTUAL PROPERTY RIGHTS</h2>
          <h3 className="text-lg font-semibold mb-2">Our intellectual property</h3>
          <p className="text-gray-600 mb-4">
            We are the owner or the licensee of all intellectual property rights in our Services, including all source code, databases, 
            functionality, software, website designs, audio, video, text, photographs, and graphics in the Services (collectively, the "Content"), 
            as well as the trademarks, service marks, and logos contained therein (the "Marks").
          </p>
          <p className="text-gray-600 mb-4">
            Our Content and Marks are protected by copyright and trademark laws (and various other intellectual property rights 
            and unfair competition laws) and treaties around the world.
          </p>
          <h3 className="text-lg font-semibold mb-2">Your use of our Services</h3>
          <p className="text-gray-600 mb-4">
            Subject to your compliance with these Legal Terms, including the "PROHIBITED ACTIVITIES" section below, we grant you 
            a non-exclusive, non-transferable, revocable license to:
          </p>
          <ul className="list-disc list-inside text-gray-600 mb-4 ml-4">
            <li>access the Services; and</li>
            <li>download or print a copy of any portion of the Content to which you have properly gained access,</li>
          </ul>
          <p className="text-gray-600">
            solely for your personal, non-commercial use.
          </p>
        </section>

        <section id="userreps" className="mb-8">
          <h2 className="text-xl font-bold mb-4">3. USER REPRESENTATIONS</h2>
          <p className="text-gray-600 mb-4">
            By using the Services, you represent and warrant that:
          </p>
          <ul className="list-disc list-inside text-gray-600 ml-4 space-y-2">
            <li>all registration information you submit will be true, accurate, current, and complete;</li>
            <li>you will maintain the accuracy of such information and promptly update such registration information as necessary;</li>
            <li>you have the legal capacity and you agree to comply with these Legal Terms;</li>
            <li>you are not under the age of 13;</li>
            <li>you are not a minor in the jurisdiction in which you reside, or if a minor, you have received parental permission to use the Services;</li>
            <li>you will not access the Services through automated or non-human means, whether through a bot, script or otherwise;</li>
            <li>you will not use the Services for any illegal or unauthorized purpose;</li>
            <li>your use of the Services will not violate any applicable law or regulation.</li>
          </ul>
        </section>

        <section id="userreg" className="mb-8">
          <h2 className="text-xl font-bold mb-4">4. USER REGISTRATION</h2>
          <p className="text-gray-600">
            You may be required to register to use the Services. You agree to keep your password confidential and will be responsible 
            for all use of your account and password. We reserve the right to remove, reclaim, or change a username you select if we 
            determine, in our sole discretion, that such username is inappropriate, obscene, or otherwise objectionable.
          </p>
        </section>

        <section id="purchases" className="mb-8">
          <h2 className="text-xl font-bold mb-4">5. PURCHASES AND PAYMENT</h2>
          <p className="text-gray-600 mb-4">
            You agree to provide current, complete, and accurate purchase and account information for all purchases made via the Services. 
            You further agree to promptly update account and payment information, including email address, payment method, and payment card 
            expiration date, so that we can complete your transactions and contact you as needed.
          </p>
          <p className="text-gray-600">
            You agree to pay all charges at the prices then in effect for your purchases and any applicable shipping fees, and you 
            authorize us to charge your chosen payment provider for any such amounts upon placing your order.
          </p>
        </section>

        <section id="prohibited" className="mb-8">
          <h2 className="text-xl font-bold mb-4">6. PROHIBITED ACTIVITIES</h2>
          <p className="text-gray-600 mb-4">
            You may not access or use the Services for any purpose other than that for which we make the Services available. 
            The Services may not be used in connection with any commercial endeavors except those that are specifically endorsed 
            or approved by us.
          </p>
          <p className="text-gray-600">
            As a user of the Services, you agree not to systematically retrieve data or other content from the Services to create 
            or compile, directly or indirectly, a collection, compilation, database, or directory without written permission from us.
          </p>
        </section>

        <section id="ugc" className="mb-8">
          <h2 className="text-xl font-bold mb-4">7. USER GENERATED CONTRIBUTIONS</h2>
          <p className="text-gray-600">
            The Services does not offer users to submit or post content. We may provide you with the opportunity to create, submit, 
            post, display, transmit, perform, publish, distribute, or broadcast content and materials to us or on the Services.
          </p>
        </section>

        <section id="license" className="mb-8">
          <h2 className="text-xl font-bold mb-4">8. CONTRIBUTION LICENSE</h2>
          <p className="text-gray-600">
            You and Services agree that we may access, store, process, and use any information and personal data that you provide 
            following the terms of the Privacy Policy and your choices.
          </p>
        </section>

        <section id="sitemanage" className="mb-8">
          <h2 className="text-xl font-bold mb-4">9. SERVICES MANAGEMENT</h2>
          <p className="text-gray-600">
            We reserve the right, but not the obligation, to: (1) monitor the Services for violations of these Legal Terms; 
            (2) take appropriate legal action against anyone who, in our sole discretion, violates the law or these Legal Terms; 
            (3) refuse, restrict access to, limit the availability of, or disable any of your Contributions or any portion thereof; 
            (4) remove from the Services or otherwise disable all files and content that are excessive in size or are in any way 
            burdensome to our systems.
          </p>
        </section>

        <section id="terms" className="mb-8">
          <h2 className="text-xl font-bold mb-4">10. TERM AND TERMINATION</h2>
          <p className="text-gray-600 mb-4">
            These Legal Terms shall remain in full force and effect while you use the Services. WITHOUT LIMITING ANY OTHER PROVISION 
            OF THESE LEGAL TERMS, WE RESERVE THE RIGHT TO, IN OUR SOLE DISCRETION AND WITHOUT NOTICE OR LIABILITY, DENY ACCESS TO 
            AND USE OF THE SERVICES, TO ANY PERSON FOR ANY REASON OR FOR NO REASON.
          </p>
          <p className="text-gray-600">
            If we terminate or suspend your account for any reason, you are prohibited from registering and creating a new account 
            under your name, a fake or borrowed name, or the name of any third party.
          </p>
        </section>

        <section id="modifications" className="mb-8">
          <h2 className="text-xl font-bold mb-4">11. MODIFICATIONS AND INTERRUPTIONS</h2>
          <p className="text-gray-600">
            We reserve the right to change, modify, or remove the contents of the Services at any time or for any reason at our 
            sole discretion without notice. We also reserve the right to modify or discontinue all or part of the Services without 
            notice at any time. We will not be liable to you or any third party for any modification, price change, suspension, 
            or discontinuance of the Services.
          </p>
        </section>

        <section id="law" className="mb-8">
          <h2 className="text-xl font-bold mb-4">12. GOVERNING LAW</h2>
          <p className="text-gray-600">
            These Legal Terms shall be governed by and defined following the laws of Russia. Hokkaido Tours and yourself irrevocably 
            consent that the courts of Russia shall have exclusive jurisdiction to resolve any dispute which may arise in connection 
            with these Legal Terms.
          </p>
        </section>

        <section id="disputes" className="mb-8">
          <h2 className="text-xl font-bold mb-4">13. DISPUTE RESOLUTION</h2>
          <p className="text-gray-600">
            Any legal action of whatever nature brought by either you or us shall be commenced or prosecuted in the state and 
            federal courts located in Russia, and the Parties hereby consent to, and waive all defenses of lack of personal 
            jurisdiction and forum non conveniens with respect to venue and jurisdiction in such courts.
          </p>
        </section>

        <section id="corrections" className="mb-8">
          <h2 className="text-xl font-bold mb-4">14. CORRECTIONS</h2>
          <p className="text-gray-600">
            There may be information on the Services that contains typographical errors, inaccuracies, or omissions, including 
            descriptions, pricing, availability, and various other information. We reserve the right to correct any errors, 
            inaccuracies, or omissions and to change or update the information on the Services at any time, without prior notice.
          </p>
        </section>

        <section id="disclaimer" className="mb-8">
          <h2 className="text-xl font-bold mb-4">15. DISCLAIMER</h2>
          <p className="text-gray-600">
            THE SERVICES ARE PROVIDED ON AN AS-IS AND AS-AVAILABLE BASIS. YOU AGREE THAT YOUR USE OF THE SERVICES WILL BE AT 
            YOUR SOLE RISK. TO THE FULLEST EXTENT PERMITTED BY LAW, WE DISCLAIM ALL WARRANTIES, EXPRESS OR IMPLIED, IN CONNECTION 
            WITH THE SERVICES AND YOUR USE THEREOF.
          </p>
        </section>

        <section id="liability" className="mb-8">
          <h2 className="text-xl font-bold mb-4">16. LIMITATIONS OF LIABILITY</h2>
          <p className="text-gray-600">
            IN NO EVENT WILL WE OR OUR DIRECTORS, EMPLOYEES, OR AGENTS BE LIABLE TO YOU OR ANY THIRD PARTY FOR ANY DIRECT, INDIRECT, 
            CONSEQUENTIAL, EXEMPLARY, INCIDENTAL, SPECIAL, OR PUNITIVE DAMAGES, INCLUDING LOST PROFIT, LOST REVENUE, LOSS OF DATA, 
            OR OTHER DAMAGES ARISING FROM YOUR USE OF THE SERVICES.
          </p>
        </section>

        <section id="indemnification" className="mb-8">
          <h2 className="text-xl font-bold mb-4">17. INDEMNIFICATION</h2>
          <p className="text-gray-600">
            You agree to defend, indemnify, and hold us harmless, including our subsidiaries, affiliates, and all of our respective 
            officers, agents, partners, and employees, from and against any loss, damage, liability, claim, or demand, including 
            reasonable attorneys' fees and expenses, made by any third party due to or arising out of your use of the Services.
          </p>
        </section>

        <section id="userdata" className="mb-8">
          <h2 className="text-xl font-bold mb-4">18. USER DATA</h2>
          <p className="text-gray-600">
            We will maintain certain data that you transmit to the Services for the purpose of managing the performance of the 
            Services, as well as data relating to your use of the Services. Although we perform regular routine backups of data, 
            you are solely responsible for all data that you transmit or that relates to any activity you have undertaken using 
            the Services.
          </p>
        </section>

        <section id="electronic" className="mb-8">
          <h2 className="text-xl font-bold mb-4">19. ELECTRONIC COMMUNICATIONS, TRANSACTIONS, AND SIGNATURES</h2>
          <p className="text-gray-600">
            Visiting the Services, sending us emails, and completing online forms constitute electronic communications. You consent 
            to receive electronic communications, and you agree that all agreements, notices, disclosures, and other communications 
            we provide to you electronically, via email and on the Services, satisfy any legal requirement that such communication 
            be in writing.
          </p>
        </section>

        <section id="misc" className="mb-8">
          <h2 className="text-xl font-bold mb-4">20. MISCELLANEOUS</h2>
          <p className="text-gray-600">
            These Legal Terms and any policies or operating rules posted by us on the Services or in respect to the Services 
            constitute the entire agreement and understanding between you and us. Our failure to exercise or enforce any right 
            or provision of these Legal Terms shall not operate as a waiver of such right or provision.
          </p>
        </section>

        <section id="contact" className="mb-8">
          <h2 className="text-xl font-bold mb-4">21. CONTACT US</h2>
          <p className="text-gray-600 mb-4">
            In order to resolve a complaint regarding the Services or to receive further information regarding use of the Services, 
            please contact us at:
          </p>
          <div className="text-gray-600">
            <p><strong>Hokkaido Tours</strong></p>
            <p>Lomonosova 9</p>
            <p>Saint-Petersburg, Leningradskaya oblast' 192007</p>
            <p>Russia</p>
            <p>Phone: 89006662505</p>
            <p>Email: <a href="mailto:zzisst@mail.ru" className="text-blue-600 hover:underline">zzisst@mail.ru</a></p>
          </div>
        </section>

        <div className="text-center mt-8">
          <Link to="/" className="text-blue-600 hover:underline">
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}
